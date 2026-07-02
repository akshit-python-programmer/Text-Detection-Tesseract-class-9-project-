# Text Detection using Tesseract

A tiny OpenCV + Tesseract OCR project that finds words in an image (or a live
webcam feed) and draws a bounding box around each detected word with its text
label on top.

## A note on where this came from

I built this back in **2021, around class 8**, when I was first messing around
with OpenCV and computer vision. It's a simple project — but it was one of the
first times I got a computer to "read" the world back to me, and that little
`imshow` window with boxes drawn around every word felt like magic at the time.

I'm putting it up now, years later, mostly as a time capsule. My projects today
are a lot more involved, but I have a soft spot for this one. Everyone starts
somewhere, and this is one of my somewheres. The code here is kept **exactly as I
originally wrote it** — quirks and all — because rewriting it would defeat the
point.

_(File timestamps put the original work in April–July 2021.)_

## What it does

There are two scripts:

- **`TextDetection.py`** — runs OCR on a static image (`imgs/1.png`), then loops
  over every detected word and draws a rectangle + the recognized text on the
  image. Result shows up in an OpenCV window.
- **`CamTextDetection.py`** — the same idea, but on your webcam. It shows a live
  feed with a "Press Space to Run!" prompt; hitting space triggers OCR on the
  current frame, and `Esc` quits.

The test image (`imgs/1.png`) contains a mix of words and numbers so you can see
both text and digit detection working.

## How it works

The core trick is `pytesseract.image_to_data()`, which returns Tesseract's
detection results as a table — one row per detected chunk, including the bounding
box coordinates and the recognized text. The code parses that table and uses
OpenCV to draw the boxes:

```python
boxes = pytesseract.image_to_data(img)
for x, b in enumerate(boxes.splitlines()):
    if x != 0:                       # skip the header row
        b = b.split()
        if len(b) == 12:             # only rows that actually have a word
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            cv2.rectangle(img, (x, y), (w + x, y + h), (255, 0, 0), 3)
            cv2.putText(img, b[11], (x, y),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
```

`pytesseract` is just a wrapper — the actual OCR is done by the **Tesseract**
engine, which has to be installed separately (see below). There's also
commented-out code in `TextDetection.py` showing the character-level version
(`image_to_boxes`) I was experimenting with.

## Project structure

```
Text Detection using Tesseract/
├── TextDetection.py      # OCR on a static image
├── CamTextDetection.py   # OCR on a live webcam feed
├── imgs/
│   └── 1.png             # sample test image (words + numbers)
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation & usage

**1. Install the Tesseract OCR engine** (this is separate from the Python
package):

- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- macOS: `brew install tesseract`
- Linux: `sudo apt install tesseract-ocr`

**2. Clone and install the Python dependencies:**

```bash
git clone https://github.com/<your-username>/text-detection-tesseract.git
cd text-detection-tesseract
pip install -r requirements.txt
```

**3. Point the code at your Tesseract install.** Both scripts hard-code the path:

```python
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
```

Update that line to wherever Tesseract lives on your machine (on macOS/Linux it's
usually just `tesseract` on your PATH, so you can point it there or drop the line
entirely).

**4. Run it:**

```bash
python TextDetection.py       # static image
python CamTextDetection.py    # webcam (Space = run OCR, Esc = quit)
```

## Future scope

Honest list of things I'd improve if I revisited this properly:

- The Tesseract path is hard-coded for Windows — it should be configurable or
  auto-detected.
- `CamTextDetection.py` imports `keyboard` but never uses it, and the spacebar
  toggle logic is a little tangled — leftovers from experimenting. Kept as-is on
  purpose.
- Add basic preprocessing (grayscale, thresholding) before OCR — Tesseract is a
  lot more accurate on clean, high-contrast input.
- Filter detections by Tesseract's confidence score to drop the junk boxes.

## Author

**Akshit** — originally built in 2021 as an early CV experiment.

- GitHub: [@&lt;your-username&gt;](https://github.com/&lt;your-username&gt;)
