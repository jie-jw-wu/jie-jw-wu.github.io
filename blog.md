---
layout: sidebar
title: Blog
permalink: /blog.html
---

<h2 id="blog">Blog</h2>

Occasional writing on research, careers, and the intersection of software engineering and AI.

<div class="post-list">
{% for post in site.posts %}
  <div class="post-entry">
    <div class="post-date">{{ post.date | date: "%B %-d, %Y" }}</div>
    <a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    {% if post.description %}<div class="post-summary">{{ post.description }}</div>{% endif %}
  </div>
{% endfor %}
</div>
