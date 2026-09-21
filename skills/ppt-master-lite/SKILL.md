---
name: ppt-master-lite
description: Use when making small offline HTML slide decks.
version: 1.0.0
author: Rogelio Macias / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [presentation, slides, html, deck]
---

# PPT Master Lite

Use this skill when the user asks for a small presentation, slide deck, or HTML slideshow.

## Safety and scope

- Work only with user-provided text.
- Do not fetch URLs, load remote assets, call external programs, execute shell commands, or modify files outside the requested output directory.
- Generate a single self-contained HTML file with inline CSS and text only.
- Do not invent facts, sources, figures, or images.

## Procedure

1. Convert the user's outline into 3–8 slides.
2. Keep one idea per slide and use concise Spanish unless the user requests another language.
3. Write a JSON input file containing `title`, `subtitle`, and `slides`; each slide has `title` and `bullets`.
4. Run `scripts/generate_html.py INPUT.json OUTPUT.html`.
5. Verify that the output exists, is non-empty, contains the requested title, and has the expected slide count.
6. Deliver the output path. The file works offline in a browser.

## Input format

```json
{"title":"Título","subtitle":"Subtítulo","slides":[{"title":"Idea 1","bullets":["Punto A","Punto B"]}]}
```

## Controls

- Arrow Left/Right or Page Up/Page Down: navigate slides.
- Home/End: first/last slide.
- The current slide number is shown at the bottom.
