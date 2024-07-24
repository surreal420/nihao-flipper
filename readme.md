# Image Flipper

This is a simple GUI application for flipping images along a selected axis using Python and Tkinter.

## Features

- Load images from files, clipboard or simply drag&drop
- Flip images horizontally or vertically
- Save flipped images to disk
- Copy flipped images to clipboard

## Requirements

- Python 3.x
- Required Python libraries listed in `requirements.txt`

## Run

To run this application, you need Python and the following dependencies:

```bash
pip install -r requirements.txt
```

Then:

```bash
python3 nihao.py
```

## Compile

You will need to install `pyinstaller`.

```bash
pip install pyinstaller
```

Then, download `hook-tkinterdnd2.py` from [here](https://github.com/pmgagne/tkinterdnd2/blob/master/hook-tkinterdnd2.py).

Put it in the same folder of `nihao.py` and run:

```bash
pyinstaller nihao.py --noconsole --onefile --collect-all TkinterDnD2 --icon=logo.ico --additional-hooks-dir=.
```