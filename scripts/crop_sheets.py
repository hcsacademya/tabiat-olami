"""ChatGPT chizgan umumiy rasmlarni alohida rasmlarga qirqadi.

Har bir umumiy rasm (sheet) art/sheets.json da yozilgan: fayl nomi va
undagi obyektlar tartibi (yuqori qator chapdan o‘ngga, keyin pastki qator).
Natija public/images/<nom>.webp ga kvadrat ko‘rinishda saqlanadi.

Ishlatish:
    pip install pillow numpy
    python scripts/crop_sheets.py
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "art" / "sheets.json"
SHEETS_DIR = ROOT / "art" / "sheets"
OUT_DIR = ROOT / "public" / "images"

EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")

SIZE = 768          # chiqadigan kvadrat rasm tomoni (px)
PADDING = 0.08      # obyekt atrofidagi bo‘sh joy, tomonga nisbatan
BG_TOLERANCE = 40   # fon rangidan shuncha farq qilgan piksel — obyekt
PART_GAP = 0.03     # obyektdan shuncha yaqin turgan qism unga qo‘shiladi
MIN_CUT = 0.005     # obyektlar orasidagi eng tor ruxsat etilgan oraliq
MIN_MASS = 0.02     # eng kattasining 2% idan kichik dog‘lar tashlanadi


def load_rgb(path):
    img = Image.open(path)
    img.load()

    # Shaffof fonni oq qilamiz.
    if img.mode in ("RGBA", "LA", "P"):
        rgba = img.convert("RGBA")
        white = Image.new("RGBA", rgba.size, "white")
        img = Image.alpha_composite(white, rgba)

    return img.convert("RGB")


def background_color(px):
    border = np.concatenate([px[0], px[-1], px[:, 0], px[:, -1]])
    return np.median(border, axis=0).astype(np.int16)


def foreground_mask(px, bg):
    diff = np.abs(px.astype(np.int16) - bg).max(axis=2)
    return diff > BG_TOLERANCE


def segments(profile, min_gap, noise=None):
    """Profilda obyekt bor oraliqlarni [(start, end), ...] qaytaradi."""
    if noise is None:
        noise = max(2, int(len(profile) * 0.002))
    filled = profile > noise

    found = []
    start = None
    for i, value in enumerate(filled):
        if value and start is None:
            start = i
        elif not value and start is not None:
            found.append([start, i])
            start = None
    if start is not None:
        found.append([start, len(filled)])

    merged = []
    for seg in found:
        if merged and seg[0] - merged[-1][1] < min_gap:
            merged[-1][1] = seg[1]
        else:
            merged.append(seg)

    if not merged:
        return []

    masses = [int(profile[a:b].sum()) for a, b in merged]
    biggest = max(masses)
    return [
        (a, b)
        for (a, b), mass in zip(merged, masses)
        if mass >= biggest * MIN_MASS
    ]


def tight_box(mask, left, top, right, bottom):
    """Berilgan katak ichidagi obyektning aniq chegarasi.

    Obyektga yaqin turgan mayda qismlar (dum, mo‘ylov, barg) ham kiradi,
    uzoqdagi mayda dog‘lar tashlanadi.
    """
    gap = int(max(mask.shape) * PART_GAP)
    cell = mask[top:bottom, left:right]
    rows = segments(cell.sum(axis=1), gap, noise=0)
    cols = segments(cell.sum(axis=0), gap, noise=0)
    if not rows or not cols:
        return None
    return (
        left + cols[0][0],
        top + rows[0][0],
        left + cols[-1][1],
        top + rows[-1][1],
    )


def cuts(profile, count):
    """Profilni `count` bo‘lakka eng keng oq oraliqlarning o‘rtasidan bo‘ladi.

    Chegaralar ro‘yxatini [0, ..., len(profile)] qaytaradi.
    """
    segs = segments(profile, 1)
    if len(segs) < count:
        return None

    gaps = sorted(
        range(len(segs) - 1),
        key=lambda i: segs[i + 1][0] - segs[i][1],
        reverse=True,
    )[:count - 1]

    min_cut = max(2, int(len(profile) * MIN_CUT))
    if any(segs[i + 1][0] - segs[i][1] < min_cut for i in gaps):
        return None

    middles = sorted((segs[i][1] + segs[i + 1][0]) // 2 for i in gaps)
    return [0] + middles + [len(profile)]


def split(mask, outer, inner):
    """Avval `outer` ta qatorga, keyin har qatorni `inner` ta katakka bo‘ladi."""
    row_cuts = cuts(mask.sum(axis=1), outer)
    if row_cuts is None:
        return None

    boxes = []
    for top, bottom in zip(row_cuts, row_cuts[1:]):
        col_cuts = cuts(mask[top:bottom].sum(axis=0), inner)
        if col_cuts is None:
            return None
        boxes.extend(
            (left, top, right, bottom)
            for left, right in zip(col_cuts, col_cuts[1:])
        )
    return boxes


def detect_auto(mask, columns, rows):
    """Obyektlarni ular orasidagi oq bo‘shliqlar bo‘yicha topadi."""
    boxes = split(mask, rows, columns)

    if boxes is None:
        # Baland obyekt (masalan, jirafa) qatorlar orasidagi bo‘shliqni
        # yopib qo‘ysa, avval ustunlarga bo‘lib ko‘ramiz.
        flipped = split(mask.T, columns, rows)
        if flipped is None:
            return None
        flipped = [(t, l, b, r) for l, t, r, b in flipped]
        boxes = [
            flipped[c * rows + r]
            for r in range(rows)
            for c in range(columns)
        ]

    return [tight_box(mask, *box) for box in boxes]


def detect_grid(mask, columns, rows):
    """Zaxira usul: rasmni teng kataklarga bo‘lib, har biridan obyektni oladi."""
    h, w = mask.shape
    boxes = []
    for r in range(rows):
        for c in range(columns):
            boxes.append(tight_box(
                mask,
                w * c // columns,
                h * r // rows,
                w * (c + 1) // columns,
                h * (r + 1) // rows,
            ))
    return boxes


def save_item(img, bg, box, path):
    piece = img.crop(box)
    side = int(max(piece.width, piece.height) * (1 + 2 * PADDING))

    canvas = Image.new("RGB", (side, side), tuple(int(c) for c in bg))
    canvas.paste(
        piece,
        ((side - piece.width) // 2, (side - piece.height) // 2),
    )
    canvas = canvas.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    canvas.save(path, "WEBP", quality=85, method=6)


def find_sheet(stem):
    for ext in EXTENSIONS:
        path = SHEETS_DIR / f"{stem}{ext}"
        if path.exists():
            return path
    return None


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    failed = False

    for sheet in config["sheets"]:
        columns = sheet.get("columns", config["columns"])
        rows = sheet.get("rows", config["rows"])
        items = sheet["items"]

        path = find_sheet(sheet["sheet"])
        if path is None:
            print(f"[{sheet['sheet']}] rasm yo‘q, o‘tkazib yuborildi")
            continue

        if len(items) != columns * rows:
            print(
                f"[{sheet['sheet']}] XATO: {columns}x{rows} katakka "
                f"{len(items)} ta nom berilgan"
            )
            failed = True
            continue

        img = load_rgb(path)
        px = np.asarray(img)
        bg = background_color(px)
        mask = foreground_mask(px, bg)

        boxes = detect_auto(mask, columns, rows)
        method = "avtomatik"
        if boxes is None:
            boxes = detect_grid(mask, columns, rows)
            method = "teng kataklar (tekshirib ko‘ring!)"

        if any(box is None for box in boxes):
            print(f"[{sheet['sheet']}] XATO: ba’zi kataklar bo‘sh")
            failed = True
            continue

        for name, box in zip(items, boxes):
            save_item(img, bg, box, OUT_DIR / f"{name}.webp")

        print(f"[{sheet['sheet']}] {len(items)} ta rasm saqlandi, usul: {method}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
