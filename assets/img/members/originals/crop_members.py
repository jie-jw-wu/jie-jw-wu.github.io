"""Crop each member headshot to a square with the face at a uniform size.

The sources vary wildly (389px square selfie vs 4694x3130 studio shot), so a
plain center crop would leave heads at very different scales. We detect the
face, then pick a crop side of face_width / TARGET_FACE_RATIO and sit the face
slightly above centre, clamping to the image edges.
"""
import cv2
import numpy as np
from PIL import Image, ImageOps

SRC = "/home/user/jie-jw-wu.github.io/assets/img/"
OUT = "/home/user/jie-jw-wu.github.io/assets/img/members/"

# name in repo -> source file
MEMBERS = {
    "josh-dafoe": "josh.jfif",
    "joshana-shakya": "joshana.jpg",
    "indrajeet-roy": "indrajeet.png",
    "gabe-dautovi": "gabe.jpg",
    "andrew-sadler": "andrew.jfif",
}

TARGET_FACE_RATIO = 0.47   # face width as a fraction of the square
FACE_CENTER_Y = 0.47       # where the face centre sits vertically in the square
SIZE = 240                 # output pixels (56px avatar at 4x)

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


for name, src in MEMBERS.items():
    im = ImageOps.exif_transpose(Image.open(SRC + src)).convert("RGB")
    w, h = im.size
    fx, fy, fw, fh = largest_face(np.array(im))
    cx, cy = fx + fw / 2, fy + fh / 2

    side = min(fw / TARGET_FACE_RATIO, w, h)
    x0 = min(max(cx - side / 2, 0), w - side)
    y0 = min(max(cy - side * FACE_CENTER_Y, 0), h - side)

    crop = im.crop((round(x0), round(y0), round(x0 + side), round(y0 + side)))
    crop = crop.resize((SIZE, SIZE), Image.LANCZOS)
    crop.save(OUT + name + ".jpg", "JPEG", quality=88, optimize=True,
              progressive=True)
    print(f"{name:16s} src {w}x{h} face {fw}px -> side {side:.0f} "
          f"(face {fw / side:.0%} of frame)")
