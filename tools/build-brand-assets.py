"""Builds the brand assets from Aleida's own public Google Maps photos.

The source photos live in tools/source-photos/ (see README). Everything the site
shows as "theirs" is cut from those files here:

  logo.webp          the circular badge, paper background removed
  menu-script.webp   the hand-lettered "Menú"
  floral-*.webp      the watercolour florals from the printed menu
  dish-*.webp        real dishes they have photographed
  hero.webp          the terrace at dusk
  og.jpg             social preview card
  favicon / apple-touch-icon

    pip install pillow numpy
    python tools/build-brand-assets.py
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source-photos")
OUT = os.path.join(os.path.dirname(HERE), "app", "img")

MENU = "menu.jpg"        # photo of the printed menu
HOTCAKES = "hotcakes.jpg"
CHILAQUILES = "chilaquiles.jpg"
CAFE = "cafe.jpg"
TERRACE = "terrace.jpg"


def unmultiply_white(im, floor=0.06):
    """White paper becomes transparent; ink keeps its colour."""
    rgb = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    minc = rgb.min(axis=2)
    alpha = np.clip(((1.0 - minc) - floor) / (1.0 - floor), 0.0, 1.0)
    safe = np.maximum(alpha, 1e-5)[..., None]
    out = np.clip((rgb - (1.0 - alpha)[..., None]) / safe, 0.0, 1.0)
    return Image.fromarray(
        (np.concatenate([out, alpha[..., None]], axis=2) * 255).astype(np.uint8), "RGBA"
    )


def build_logo(menu):
    """The badge is a black stamp; the printed florals overlap its top-right.

    Two things remove them: the logo is pure black ink, so anything saturated is
    foliage, and nothing of the logo lives outside its own outer ring, so the
    circular mask is cut to that ring instead of to the crop.
    """
    region = menu.crop((430, 10, 720, 295))
    gray = np.asarray(region.convert("L"))
    ys, xs = np.nonzero(gray < 110)  # the ring and lettering, not the foliage
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    ring_r = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2

    margin = 1.06
    box = (int(cx - ring_r * margin), int(cy - ring_r * margin),
           int(cx + ring_r * margin), int(cy + ring_r * margin))
    size = 560
    badge = region.crop(box).resize((size, size), Image.LANCZOS)
    badge = ImageEnhance.Contrast(badge).enhance(1.45)

    rgb = np.asarray(badge.convert("RGB")).astype(np.float32)
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-5), 0.0)
    # even washed-out leaf highlights keep a warm/green cast; the stamp is neutral
    foliage = ((green - blue) > 8) | ((red - blue) > 12) | ((sat > 0.13) & (mx > 56))

    badge = unmultiply_white(badge, floor=0.12)
    alpha = np.asarray(badge.getchannel("A")).astype(np.float32)
    alpha[foliage] = 0.0
    alpha[alpha < 36] = 0.0  # faint halo left by the paper texture

    # clip exactly at the outer ring, where the crop margin (and its leftovers) starts
    clip = Image.new("L", (size, size), 0)
    inset = (size / 2) * (1 - 1 / margin)
    ImageDraw.Draw(clip).ellipse((inset, inset, size - inset, size - inset), fill=255)
    alpha = np.minimum(alpha, np.asarray(clip).astype(np.float32))

    badge.putalpha(Image.fromarray(alpha.astype(np.uint8)))
    badge.save(os.path.join(OUT, "logo.webp"), quality=92, method=4)


def build_script(menu):
    im = ImageEnhance.Contrast(menu.crop((430, 300, 700, 405))).enhance(1.4)
    im = unmultiply_white(im, floor=0.12)
    im.resize((760, int(760 * im.size[1] / im.size[0])), Image.LANCZOS).save(
        os.path.join(OUT, "menu-script.webp"), quality=92, method=4
    )


def build_floral(menu, box, width, name):
    im = unmultiply_white(menu.crop(box), floor=0.05)
    im.resize((width, int(width * im.size[1] / im.size[0])), Image.LANCZOS).save(
        os.path.join(OUT, name), quality=84, method=4
    )


def build_photo(src, box, size, name, quality=80):
    im = Image.open(os.path.join(SRC, src)).convert("RGB").crop(box).resize(size, Image.LANCZOS)
    im.save(os.path.join(OUT, name), quality=quality, method=4)


def build_icons():
    logo = Image.open(os.path.join(OUT, "logo.webp")).convert("RGBA")
    for size, name in ((64, "favicon.png"), (180, "apple-touch-icon.png")):
        canvas = Image.new("RGB", (size, size), (253, 251, 247))
        inner = int(size * 0.8)
        mark = logo.resize((inner, inner), Image.LANCZOS)
        canvas.paste(mark, (int(size * 0.1), int(size * 0.1)), mark)
        canvas.save(os.path.join(OUT, name))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    menu = Image.open(os.path.join(SRC, MENU))  # 1080 x 1535

    build_logo(menu)
    build_script(menu)
    build_floral(menu, (748, 0, 1080, 425), 660, "floral-top.webp")
    build_floral(menu, (0, 1298, 225, 1492), 380, "floral-left.webp")
    build_floral(menu, (845, 1372, 1080, 1520), 430, "floral-right.webp")

    build_photo(HOTCAKES, (150, 620, 1350, 1820), (820, 820), "dish-hotcakes.webp")
    build_photo(CHILAQUILES, (430, 800, 1400, 1770), (820, 820), "dish-chilaquiles.webp")
    build_photo(CAFE, (300, 120, 1150, 970), (820, 820), "dish-cafe.webp")
    build_photo(TERRACE, (640, 350, 1400, 820), (1280, 792), "hero.webp")
    build_photo(HOTCAKES, (60, 700, 1400, 1404), (1200, 630), "og.jpg", quality=82)

    build_icons()

    for f in sorted(os.listdir(OUT)):
        print(f, round(os.path.getsize(os.path.join(OUT, f)) / 1024, 1), "KB")
