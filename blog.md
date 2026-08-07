---
layout: standalone
title: Blog | Jie JW Wu
permalink: /blog.html
---

# Blog

Occasional writing on research, careers, and the intersection of software engineering and AI.

{% for post in site.posts %}
<div style="margin-bottom: 24px;">
  <div style="color: #888; font-size: 13px;">{{ post.date | date: "%B %-d, %Y" }}</div>
  <a href="{{ post.url | relative_url }}" style="font-size: 17px; font-weight: 600;">{{ post.title }}</a>
  {% if post.description %}<div style="margin-top: 4px;">{{ post.description }}</div>{% endif %}
</div>
{% endfor %}

---

[← Back to Homepage](index.html)
