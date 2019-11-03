# My Simple Website

# Static Site Generator

A generator(`build.py` or `build.sh`) generate static html files based on top.html, bottom.html, and a content htlm.

## build.py

This script simply combines top.html, a content html, and bottom.html and write output
to a html file. More functional than `build.sh`

## build.sh

This script simply combines top.html, a content html, and bottom.html and write output
to a html file

# Directory Structure

```text
 my_homepage
 .
├── README.md
|
├── build.py
├── build.sh
|
├── docs
│   ├── index.html
│   ├── blog.html
│   ├── projects.html
│   ├── contact.html
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
├── index.html
├── blog.html
├── projects.html
├── contact.html
|
├── contents
│   ├── blog.html
│   ├── contact.html
│   ├── index.html
│   └── projects.html
|
├── templates
│   ├── bottom.html
│   └── top.html
└── tests
    └── test_build.py
```

# Color Scheme

[Selected Color Palette](https://colorhunt.co/palette/158293)
- #42b883
- #347474
- #35495e
- #ff7e67

# Fonts

- Body:  Arial, Helvetica, sans-serif

- Lato Bold, sans-serif

- Monospace: Courier New
