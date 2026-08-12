"""Crop each member headshot to a square with the face at a uniform size.

The sources vary wildly (389px square selfie vs 4694x3130 studio shot), so a
plain center crop would leave heads at very different scales. We detect the
face, then pick a crop side of face_width / TARGET_FACE_RATIO and sit the face
slightly above centre, clamping to the image edges.
"""
import os

import cv2
import numpy as np
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.normpath(os.path.join(HERE, "..", ".."))   # assets/img
OUT = os.path.join(IMG, "members")

# avatar name -> source, relative to assets/img
MEMBERS = {
    # Dr. Wu's photo doubles as the site-wide avatar in _config.yml, so it
    # stays where it is rather than moving into originals/.
    "jie-wu": "jw_pic.jpeg",
    "josh-dafoe": "members/originals/josh.jfif",
    "joshana-shakya": "members/originals/joshana.jpg",
    "indrajeet-roy": "members/originals/indrajeet.png",
    "gabe-dautovi": "members/originals/gabe.jpg",
    "andrew-sadler": "members/originals/andrew.jfif",
}

TARGET_FACE_RATIO = 0.47   # face width as a fraction of the square
FACE_CENTER_Y = 0.47       # where the face centre sits vertically in the square
SIZE = 336                 # output pixels (84px avatar at 4x)

# Some sources are framed so tightly that the ideal crop runs off the edge --
# Indrajeet's hair starts 20px from the top, leaving no headroom to give him.
# Where the edge we would run past is plain backdrop, we can extend it and keep
# the head properly centred. Where it is not (a shoulder, a wall), extending
# would smear real content, so we fall back to clamping the crop inside the
# image and accept the off-centre framing.
BACKDROP_TOL = 26       # per-channel distance that still counts as backdrop
BACKDROP_MIN = 0.90     # fraction of an edge that must be backdrop to extend it
MAX_PAD = 0.15          # never invent more than this fraction of the crop

cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def largest_face(rgb):
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape
    faces = cascade.detectMultiScale(
        gray, scaleFactor=1.08, minNeighbors=6,
        minSize=(max(24, w // 20), max(24, h // 20)),
    )
    if len(faces) == 0:
        raise SystemExit("no face found")
    return max(faces, key=lambda r: r[2] * r[3])


def backdrop_color(arr):
    """Median of the one-pixel border ring, robust to a subject touching it."""
    ring = np.concatenate([arr[0], arr[-1], arr[:, 0], arr[:, -1]])
    return np.median(ring, axis=0)


def is_backdrop(line, bg):
    return (np.abs(line.astype(int) - bg).max(axis=1)
            <= BACKDROP_TOL).mean() >= BACKDROP_MIN


for name, src in MEMBERS.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(IMG, src))).convert("RGB")
    arr = np.array(im)
    w, h = im.size
    fx, fy, fw, fh = largest_face(arr)
    cx, cy = fx + fw / 2, fy + fh / 2

    side = fw / TARGET_FACE_RATIO
    pad = {
        "top": max(0.0, side * FACE_CENTER_Y - cy),
        "bottom": max(0.0, cy + side * (1 - FACE_CENTER_Y) - h),
        "left": max(0.0, side / 2 - cx),
        "right": max(0.0, cx + side / 2 - w),
    }
    edges = {"top": arr[0], "bottom": arr[-1],
             "left": arr[:, 0], "right": arr[:, -1]}
    bg = backdrop_color(arr)
    wanted = {k: v for k, v in pad.items() if v > 0.5}
    extend = (wanted
              and max(wanted.values()) <= side * MAX_PAD
              and all(is_backdrop(edges[k], bg) for k in wanted))

    if extend:
        t, b = int(np.ceil(pad["top"])), int(np.ceil(pad["bottom"]))
        l, r = int(np.ceil(pad["left"])), int(np.ceil(pad["right"]))
        arr = cv2.copyMakeBorder(arr, t, b, l, r, cv2.BORDER_REPLICATE)
        im = Image.fromarray(arr)
        cx, cy = cx + l, cy + t
        w, h = im.size
    else:
        side = min(side, w, h)

    x0 = min(max(cx - side / 2, 0), w - side)
    y0 = min(max(cy - side * FACE_CENTER_Y, 0), h - side)

    crop = im.crop((round(x0), round(y0), round(x0 + side), round(y0 + side)))
    crop = crop.resize((SIZE, SIZE), Image.LANCZOS)
    crop.save(os.path.join(OUT, name + ".jpg"), "JPEG", quality=88,
              optimize=True, progressive=True)
    note = ("backdrop extended " + ", ".join(f"{k} {v:.0f}px"
            for k, v in sorted(wanted.items())) if extend else
            "clamped" if wanted else "fits")
    print(f"{name:16s} face {fw / side:.0%} of frame, "
          f"eyes at {(cy - y0) / side:.0%} down  [{note}]")
