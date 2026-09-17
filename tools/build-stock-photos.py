"""Turns the stock reference photos into the square thumbnails the menu uses.

These are NOT Aleida's dishes — they are Wikimedia Commons photos of the same
dish, used only so the menu reads like a menu instead of a list of cartoons.
Every one is CC BY / CC BY-SA and is credited in the page footer; see
stock-photos/CREDITS.json. Replace them with Aleida's own photos before this
goes in front of anyone.

    python tools/build-stock-photos.py
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "stock-photos")
OUT = os.path.join(os.path.dirname(HERE), "app", "img")
SIZE = 640

# key -> (horizontal focus, vertical focus) as fractions of the image
FOCUS = {
    "omelette-aleida": (0.5, 0.5),
    "omelette": (0.5, 0.55),
    "huevos-al-gusto": (0.5, 0.5),
    "huevos-motulenos": (0.5, 0.5),
    "pan-dulce": (0.5, 0.5),
    "fajitas": (0.45, 0.5),
    "pechuga-empanizada": (0.5, 0.5),
    "cordon-bleu": (0.5, 0.5),
}


def square(name, focus):
    im = Image.open(os.path.join(SRC, f"{name}.jpg")).convert("RGB")
    w, h = im.size
    side = min(w, h)
    cx, cy = focus[0] * w, focus[1] * h
    left = max(0, min(w - side, cx - side / 2))
    top = max(0, min(h - side, cy - side / 2))
    im = im.crop((int(left), int(top), int(left + side), int(top + side)))
    im = im.resize((SIZE, SIZE), Image.LANCZOS)
    path = os.path.join(OUT, f"dish-{name}.webp")
    im.save(path, quality=80, method=4)
    print(f"dish-{name}.webp", round(os.path.getsize(path) / 1024, 1), "KB")


if __name__ == "__main__":
    for key, focus in FOCUS.items():
        square(key, focus)
