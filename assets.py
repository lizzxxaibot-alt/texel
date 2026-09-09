"""Ten game assets, drawn as a SEQUENCE OF STEPS through Texel's real API.

Each asset is a list of (label, fn) where fn paints one stage onto the canvas.
The recorder captures a frame after every stage, so the video shows the artwork
actually being built - not a slideshow of finished images.

Every stroke goes through core.raster / core.canvas, the same code the modal
paint operator calls. Nothing here is drawn by hand into a bitmap.
"""
from core import raster as R
from core import tools as T
from core.canvas import Canvas

SIZE = 32


def _pal(c, *cols):
    return [c.add_colour(x) for x in cols]


# --------------------------------------------------------------------- tiles
def grass_tile(c):
    dark, mid, light, dirt = _pal(c, (54, 96, 62, 255), (74, 124, 74, 255),
                                  (108, 168, 92, 255), (118, 88, 56, 255))
    L = c.layers[0]

    def base():
        for p in R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True):
            L.set(*p, dark)

    def dither():
        for y in range(SIZE):
            for x in range(SIZE):
                if (x + y) % 2 == 0 and (x * 7 + y * 3) % 5 < 2:
                    L.set(x, y, mid)

    def blades():
        for bx, by in ((3, 6), (11, 3), (19, 9), (26, 5), (7, 20), (22, 24), (14, 15)):
            for p in R.line(bx, by, bx, by - 3):
                L.set(*p, light)
            L.set(bx - 1, by - 2, light)
            L.set(bx + 1, by - 3, light)

    def patch():
        for p in R.ellipse_box(16, 18, 27, 27, filled=True):
            L.set(*p, dirt)
        for p in R.ellipse_box(16, 18, 27, 27):
            L.set(*p, mid)

    return [("fill base", base), ("dither midtone", dither),
            ("grass blades", blades), ("dirt patch", patch)]


def brick_tile(c):
    mortar, brick, hi, lo = _pal(c, (58, 54, 58, 255), (142, 88, 74, 255),
                                 (176, 116, 96, 255), (108, 64, 54, 255))
    L = c.layers[0]

    def base():
        for p in R.rect(0, 0, SIZE - 1, SIZE - 1, filled=True):
            L.set(*p, mortar)

    def rows():
        for i, y in enumerate(range(0, SIZE, 8)):
            off = 0 if i % 2 == 0 else 8
            for x in range(-8 + off, SIZE, 16):
                for p in R.rect(x + 1, y + 1, x + 14, y + 6, filled=True):
                    L.set(*p, brick)

    def shade():
        for y in range(SIZE):
            for x in range(SIZE):
                if L.get(x, y) == brick:
                    if L.get(x, y - 1) == mortar:
                        L.set(x, y, hi)
                    elif L.get(x, y + 1) == mortar:
                        L.set(x, y, lo)

    return [("mortar bed", base), ("lay bricks", rows), ("light and shade", shade)]


# -------------------------------------------------------------------- props
def crate(c):
    wood, dark, light, iron = _pal(c, (146, 102, 58, 255), (96, 64, 34, 255),
                                   (186, 142, 88, 255), (78, 78, 88, 255))
    L = c.layers[0]

    def body():
        for p in R.rect(4, 4, 27, 27, filled=True):
            L.set(*p, wood)

    def frame():
        for p in R.rect(4, 4, 27, 27):
            L.set(*p, dark)
        for p in R.rect(5, 5, 26, 26):
            L.set(*p, light)

    def planks():
        for y in (11, 20):
            for p in R.line(5, y, 26, y):
                L.set(*p, dark)

    def cross():
        for p in R.pixel_perfect(R.line(6, 6, 25, 25)):
            L.set(*p, iron)
        for p in R.pixel_perfect(R.line(25, 6, 6, 25)):
            L.set(*p, iron)

    return [("box body", body), ("frame edges", frame),
            ("plank seams", planks), ("iron cross", cross)]


def chest(c):
    wood, dark, gold, hi = _pal(c, (128, 84, 46, 255), (74, 48, 26, 255),
                                (226, 178, 62, 255), (170, 122, 70, 255))
    L = c.layers[0]

    def base():
        for p in R.rect(4, 14, 27, 27, filled=True):
            L.set(*p, wood)
        for p in R.rect(4, 14, 27, 27):
            L.set(*p, dark)

    def lid():
        for p in R.ellipse_box(4, 6, 27, 20, filled=True):
            L.set(*p, wood)
        for p in R.ellipse_box(4, 6, 27, 20):
            L.set(*p, dark)
        for p in R.rect(4, 15, 27, 27, filled=True):
            L.set(*p, wood)
        for p in R.rect(4, 15, 27, 27):
            L.set(*p, dark)

    def bands():
        for x in (9, 22):
            for p in R.line(x, 7, x, 26):
                L.set(*p, gold)

    def lock():
        for p in R.rect(14, 16, 17, 21, filled=True):
            L.set(*p, gold)
        for p in R.rect(15, 18, 16, 19, filled=True):
            L.set(*p, dark)
        for p in R.line(6, 16, 25, 16):
            L.set(*p, hi)

    return [("chest base", base), ("domed lid", lid),
            ("gold bands", bands), ("lock plate", lock)]


def potion(c):
    glass, liquid, hi, cork = _pal(c, (92, 132, 148, 255), (196, 62, 88, 255),
                                   (236, 236, 244, 255), (142, 102, 58, 255))
    L = c.layers[0]

    def flask():
        for p in R.ellipse_box(8, 13, 23, 28, filled=True):
            L.set(*p, glass)
        for p in R.rect(13, 6, 18, 14, filled=True):
            L.set(*p, glass)

    def fill():
        for p in R.ellipse_box(10, 17, 21, 26, filled=True):
            L.set(*p, liquid)

    def stopper():
        for p in R.rect(12, 3, 19, 7, filled=True):
            L.set(*p, cork)

    def shine():
        for p in R.line(12, 18, 12, 23):
            L.set(*p, hi)
        L.set(13, 17, hi)
        for p in R.line(15, 7, 15, 11):
            L.set(*p, hi)

    return [("glass flask", flask), ("pour liquid", fill),
            ("cork stopper", stopper), ("highlights", shine)]


def sword(c):
    steel, edge, grip, gold = _pal(c, (168, 176, 190, 255), (226, 232, 240, 255),
                                   (104, 68, 40, 255), (216, 172, 60, 255))
    L = c.layers[0]

    def blade():
        for p in R.rect(14, 3, 17, 21, filled=True):
            L.set(*p, steel)
        for p in R.line(15, 2, 16, 2):
            L.set(*p, steel)

    def sharpen():
        for p in R.line(15, 3, 15, 20):
            L.set(*p, edge)
        L.set(16, 2, edge)

    def guard():
        for p in R.rect(8, 21, 23, 23, filled=True):
            L.set(*p, gold)

    def handle():
        for p in R.rect(14, 24, 17, 29, filled=True):
            L.set(*p, grip)
        for p in R.ellipse_box(13, 28, 18, 31, filled=True):
            L.set(*p, gold)

    return [("blade", blade), ("edge highlight", sharpen),
            ("crossguard", guard), ("grip and pommel", handle)]


def coin(c):
    gold, dark, hi = _pal(c, (222, 174, 54, 255), (150, 106, 26, 255),
                          (250, 226, 140, 255))
    L = c.layers[0]

    def disc():
        for p in R.ellipse_box(6, 6, 25, 25, filled=True):
            L.set(*p, gold)

    def rim():
        for p in R.ellipse_box(6, 6, 25, 25):
            L.set(*p, dark)
        for p in R.ellipse_box(9, 9, 22, 22):
            L.set(*p, dark)

    def face():
        for p in R.rect(14, 12, 17, 19, filled=True):
            L.set(*p, dark)
        for p in R.line(12, 12, 19, 12):
            L.set(*p, dark)

    def shine():
        for p in R.line(10, 11, 13, 8):
            L.set(*p, hi)
        L.set(11, 12, hi)

    return [("gold disc", disc), ("rim rings", rim),
            ("stamped face", face), ("shine", shine)]


def torch(c):
    wood, dark, flame, core = _pal(c, (118, 82, 46, 255), (74, 50, 28, 255),
                                   (238, 132, 40, 255), (252, 226, 118, 255))
    L = c.layers[0]

    def stick():
        for p in R.rect(14, 14, 17, 30, filled=True):
            L.set(*p, wood)
        for p in R.line(14, 14, 14, 30):
            L.set(*p, dark)

    def wrap():
        for y in (17, 21, 25):
            for p in R.line(13, y, 18, y):
                L.set(*p, dark)

    def fire():
        for p in R.ellipse_box(10, 3, 21, 15, filled=True):
            L.set(*p, flame)

    def heart():
        for p in R.ellipse_box(13, 6, 18, 13, filled=True):
            L.set(*p, core)

    return [("wooden shaft", stick), ("binding", wrap),
            ("flame", fire), ("hot core", heart)]


def door(c):
    wood, dark, light, iron = _pal(c, (124, 82, 46, 255), (72, 46, 26, 255),
                                   (162, 116, 70, 255), (86, 86, 96, 255))
    L = c.layers[0]

    def panel():
        for p in R.rect(5, 4, 26, 31, filled=True):
            L.set(*p, wood)
        for p in R.rect(5, 4, 26, 31):
            L.set(*p, dark)

    def arch():
        for p in R.ellipse_box(5, 1, 26, 13, filled=True):
            L.set(*p, wood)
        for p in R.ellipse_box(5, 1, 26, 13):
            L.set(*p, dark)

    def planks():
        for x in (12, 19):
            for p in R.line(x, 5, x, 30):
                L.set(*p, dark)
        for p in R.line(6, 5, 25, 5):
            L.set(*p, light)

    def hardware():
        for p in R.ellipse_box(20, 18, 24, 22, filled=True):
            L.set(*p, iron)
        for y in (9, 26):
            for p in R.line(6, y, 25, y):
                L.set(*p, iron)

    return [("door panel", panel), ("arched top", arch),
            ("plank lines", planks), ("iron fittings", hardware)]


def barrel(c):
    wood, dark, light, band = _pal(c, (140, 96, 52, 255), (84, 56, 30, 255),
                                   (176, 130, 80, 255), (92, 92, 102, 255))
    L = c.layers[0]

    def body():
        for p in R.ellipse_box(5, 3, 26, 28, filled=True):
            L.set(*p, wood)

    def staves():
        for x in (10, 15, 21):
            for p in R.line(x, 4, x, 27):
                L.set(*p, dark)
        for p in R.line(7, 4, 7, 27):
            L.set(*p, light)

    def hoops():
        for y in (8, 23):
            for p in R.line(5, y, 26, y):
                if L.get(*p):
                    L.set(*p, band)

    def top():
        for p in R.ellipse_box(8, 1, 23, 7, filled=True):
            L.set(*p, light)
        for p in R.ellipse_box(8, 1, 23, 7):
            L.set(*p, dark)

    return [("barrel body", body), ("staves", staves),
            ("iron hoops", hoops), ("open top", top)]


def gem(c):
    deep, mid, bright, spark = _pal(c, (46, 78, 152, 255), (78, 126, 210, 255),
                                    (150, 200, 246, 255), (240, 250, 255, 255))
    L = c.layers[0]

    def stone():
        for p in R.ellipse_box(7, 6, 24, 27, filled=True):
            L.set(*p, deep)

    def facets():
        for p in R.pixel_perfect(R.line(15, 7, 8, 16)):
            L.set(*p, mid)
        for p in R.pixel_perfect(R.line(16, 7, 23, 16)):
            L.set(*p, mid)
        for p in R.line(8, 17, 23, 17):
            L.set(*p, mid)

    def crown():
        for p in R.rect(12, 8, 19, 15, filled=True):
            L.set(*p, bright)

    def glint():
        for p in R.line(13, 10, 15, 10):
            L.set(*p, spark)
        L.set(13, 11, spark)
        L.set(20, 21, spark)

    return [("gem body", stone), ("facet lines", facets),
            ("crown table", crown), ("glint", glint)]


ASSETS = [
    ("grass-tile", "Grass terrain tile", grass_tile, True),
    ("brick-tile", "Stone brick tile", brick_tile, True),
    ("crate", "Wooden crate", crate, False),
    ("chest", "Treasure chest", chest, False),
    ("potion", "Health potion", potion, False),
    ("sword", "Iron sword", sword, False),
    ("coin", "Gold coin", coin, False),
    ("torch", "Wall torch", torch, False),
    ("door", "Arched door", door, False),
    ("barrel", "Oak barrel", barrel, False),
]


def build(fn):
    """Run every stage of an asset and return (canvas, [labels])."""
    c = Canvas(SIZE, SIZE)
    labels = []
    for label, step in fn(c):
        step()
        labels.append(label)
    return c, labels
