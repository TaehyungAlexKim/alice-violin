# Mini-poster — build & image credits

`violin-mini-poster.png` — 4×6" @ 300dpi (1200×1800). Generate with:
```bash
/tmp/qrvenv/bin/python build_poster.py   # needs Pillow + segno
```
Tone matches the main poster (cream + deep-navy serif + gold). **No black ink**:
all dark tones are deep navy, and the three landmark photos are rendered as a
navy↔cream **duotone** so they print on a color-only printer and look like one set.

## Image sources
- **Freiburg** (`assets/freiburg.jpg`) — "Aerial View – Freiburg im Breisgau-Münster1"
  by **Taxiarchos228**, **CC BY 3.0**, via Wikimedia Commons.
  https://commons.wikimedia.org/wiki/File:Aerial_View_-_Freiburg_im_Breisgau-M%C3%BCnster1.jpg
  → If printed/shared publicly, keep this attribution (CC BY requires credit).
- **Vancouver** (`assets/vancouver.webp`) — BC Place at night. Supplied by the user.
- **Korea** (`assets/korea.webp`) — Gyeongbokgung Palace. Supplied by the user.
  (User-supplied images: verify usage rights before wide public distribution.)

QR encodes https://taehyungalexkim.github.io/alice-violin/?ref=poster — decode-verified
from the rendered poster with OpenCV.
