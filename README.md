# My Simple Website

## Static Site Generator

A generator(`build.py` generates static html files based on base.html, and content htlm files.

### build.py

This script simply combines a template file and a content html, then replace title based on a content file
, and write to a html file.

## Directory Structure

```text
my_homepage
|
├── README.md
|
├── build.py
|
├── content
│   ├── blog.html
│   ├── contact.html
│   ├── index.html
│   └── projects.html
├── templates
│   ├── base.html
│   └── blog_base.html
|
├── docs
│   ├── index.html
│   ├── projects.html
│   ├── contact.html
│   ├── blog.html
│   ├── blog_post_1.html
│   ├── blog_post_2.html
│   ├── blog_post_3.html
│   ├── blog_post_4.html
│   ├── css
│   │   ├── blog.css
│   │   ├── contact.css
│   │   ├── main.css
│   │   ├── projects.css
│   │   └── shared.css
│   └── images
│       ├── github.svg
│       ├── linkedin.svg
│       ...
|
└── tests
    └── test_build.py
```

## Color Scheme

[Selected Color Palette](https://colorhunt.co/palette/158293)
- #FAF9FA for body background
- #347474 for a tags
- #42b883 for hovered a tags
- #B34C3B for contact page item titles

## Fonts

- Body:  Arial, Helvetica, sans-serif
- Lato Bold, sans-serif
- Monospace: Courier New
