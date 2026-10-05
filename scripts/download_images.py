import io
import json
import time
from pathlib import Path

import requests
from PIL import Image, ImageOps

API = "https://api.openverse.org/v1/images/"

OUT_DIR = Path("public/images")
MANIFEST = Path("public/images/manifest.json")

# English search terms are intentional:
# Openverse usually finds more relevant results with English names.
ITEMS = [
    (1, "Sher", "lion"),
    (2, "Fil", "African elephant"),
    (3, "Jirafa", "giraffe"),
    (4, "Zebra", "zebra"),
    (5, "Maymun", "monkey"),
    (6, "Karkidon", "rhinoceros"),
    (7, "Begemot", "hippopotamus"),
    (8, "Kiyik", "deer"),
    (9, "Gorilla", "gorilla"),
    (10, "Kenguru", "kangaroo"),

    (11, "Yo‘lbars", "tiger"),
    (12, "Bo‘ri", "wolf"),
    (13, "Tulki", "red fox"),
    (14, "Qoplon", "leopard"),
    (15, "Gepard", "cheetah"),
    (16, "Ayiq", "brown bear"),
    (17, "Sirtlon", "spotted hyena"),
    (18, "Timsoh", "crocodile"),
    (19, "Ilon", "snake"),
    (20, "Burgut", "eagle"),

    (21, "Oltinbaliq", "goldfish"),
    (22, "Akula", "great white shark"),
    (23, "Kit akulasi", "whale shark"),
    (24, "Skat", "manta ray"),
    (25, "Laqqa baliq", "catfish"),
    (26, "Forel", "trout"),
    (27, "Losos", "salmon"),
    (28, "Sazan", "common carp"),
    (29, "Tuna", "yellowfin tuna"),
    (30, "Delfin", "dolphin"),

    (31, "Burgut", "eagle"),
    (32, "Boyo‘g‘li", "great horned owl"),
    (33, "Qarg‘a", "crow"),
    (34, "Kabutar", "pigeon"),
    (35, "Laylak", "white stork"),
    (36, "Qaldirg‘och", "barn swallow"),
    (37, "To‘tiqush", "macaw parrot"),
    (38, "Tovus", "peacock"),
    (39, "Oqqush", "mute swan"),
    (40, "Flamingo", "flamingo"),

    (41, "Asalari", "honey bee"),
    (42, "Kapalak", "monarch butterfly"),
    (43, "Chumoli", "ant"),
    (44, "Qo‘ng‘iz", "ladybird beetle"),
    (45, "Chigirtka", "grasshopper"),
    (46, "Ninachi", "dragonfly"),
    (47, "Pashsha", "house fly"),
    (48, "Chivin", "mosquito"),
    (49, "Qurt", "earthworm"),
    (50, "Qo‘ng‘izcha", "ladybird"),

    (51, "Olma", "red apple"),
    (52, "Nok", "pear"),
    (53, "Apelsin", "orange fruit"),
    (54, "Banan", "banana"),
    (55, "Uzum", "table grapes"),
    (56, "Anor", "pomegranate"),
    (57, "Shaftoli", "peach"),
    (58, "Gilos", "cherry"),
    (59, "Qulupnay", "strawberry"),
    (60, "Mango", "mango"),

    (61, "Terak", "poplar tree"),
    (62, "Chinor", "plane tree"),
    (63, "Archa", "juniper tree"),
    (64, "Qayin", "birch tree"),
    (65, "Eman", "oak tree"),
    (66, "Qarag‘ay", "pine tree"),
    (67, "Tol", "willow tree"),
    (68, "Olma daraxti", "apple tree"),
    (69, "O‘rik daraxti", "apricot tree"),
    (70, "Tut daraxti", "mulberry tree"),

    (71, "Atirgul", "rose flower"),
    (72, "Lola", "tulip flower"),
    (73, "Moychechak", "chamomile flower"),
    (74, "Binafsha", "violet flower"),
    (75, "Nargiz", "daffodil flower"),
    (76, "Rayhon guli", "basil flower"),
    (77, "Boychechak", "snowdrop flower"),
    (78, "Orxideya", "orchid flower"),
    (79, "Kungaboqar", "sunflower"),
    (80, "Chinnigul", "carnation flower"),

    (81, "Aloe vera", "aloe vera plant"),
    (82, "Kaktus", "cactus plant"),
    (83, "Yalpiz", "mint plant"),
    (84, "Rayhon", "basil plant"),
    (85, "Shivit", "dill plant"),
    (86, "Petrushka", "parsley plant"),
    (87, "Makkajo‘xori", "corn plant"),
    (88, "Bug‘doy", "wheat plant"),
    (89, "Guruch o‘simligi", "rice plant"),
    (90, "Kartoshka", "potato plant"),

    (91, "Mushuk", "domestic cat"),
    (92, "It", "golden retriever dog"),
    (93, "Ot", "horse"),
    (94, "Sigir", "cow"),
    (95, "Qo‘y", "sheep"),
    (96, "Echki", "goat"),
    (97, "Quyon", "rabbit"),
    (98, "Tovuq", "domestic chicken"),
    (99, "O‘rdak", "mallard duck"),
    (100, "Eshak", "donkey"),
]


HEADERS = {
    "User-Agent": "Tabiat-Olami/1.0 educational project"
}

LICENSES = ["cc0", "by", "by-sa"]


def api_search(query, license_name):
    params = {
        "q": query,
        "license": license_name,
        "page_size": 20,
    }

    r = requests.get(
        API,
        params=params,
        headers=HEADERS,
        timeout=30,
    )
    r.raise_for_status()

    return r.json().get("results", [])


def looks_good(item):
    width = item.get("width") or 0
    height = item.get("height") or 0

    if width < 500 or height < 500:
        return False

    if item.get("watermarked") is True:
        return False

    url = item.get("url")
    if not url or not url.startswith(("http://", "https://")):
        return False

    # Avoid extremely wide/tall images.
    ratio = width / height
    if ratio < 0.45 or ratio > 2.2:
        return False

    return True


def download_image(url):
    r = requests.get(
        url,
        headers=HEADERS,
        timeout=45,
    )

    if r.status_code != 200:
        return None

    content_type = r.headers.get("content-type", "").lower()

    if "image" not in content_type:
        return None

    if len(r.content) > 15 * 1024 * 1024:
        return None

    try:
        img = Image.open(io.BytesIO(r.content))
        img.load()
        return img
    except Exception:
        return None


def optimize(img):
    img = ImageOps.exif_transpose(img)

    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    # Square educational-card format.
    img.thumbnail((700, 700), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (700, 700), "white")

    x = (700 - img.width) // 2
    y = (700 - img.height) // 2

    if img.mode == "RGBA":
        canvas.paste(img, (x, y), img)
    else:
        canvas.paste(img, (x, y))

    return canvas


def save_webp(img, path):
    # Start with quality 82 and reduce if necessary.
    for quality in (82, 76, 70, 64, 58):
        buffer = io.BytesIO()

        img.save(
            buffer,
            "WEBP",
            quality=quality,
            method=6,
        )

        data = buffer.getvalue()

        if len(data) <= 300 * 1024:
            path.write_bytes(data)
            return len(data)

    path.write_bytes(data)
    return len(data)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = []

    for number, uzbek_name, query in ITEMS:
        filename = f"{number:03d}.webp"
        output = OUT_DIR / filename

        print(f"\n[{number:03d}] {uzbek_name} -> {query}")

        selected = None

        for license_name in LICENSES:
            try:
                results = api_search(query, license_name)
            except Exception as e:
                print("API error:", e)
                continue

            for item in results:
                if looks_good(item):
                    selected = item
                    break

            if selected:
                break

            time.sleep(0.5)

        if not selected:
            print("NO SUITABLE IMAGE FOUND")
            manifest.append({
                "id": number,
                "name": uzbek_name,
                "file": filename,
                "status": "missing",
            })
            continue

        print("Selected:", selected.get("title"))
        print("License:", selected.get("license"))
        print("Source:", selected.get("provider"))

        img = download_image(selected["url"])

        if img is None:
            print("Download failed")

            manifest.append({
                "id": number,
                "name": uzbek_name,
                "file": filename,
                "status": "download_failed",
                "source_url": selected.get("url"),
            })
            continue

        optimized = optimize(img)
        size = save_webp(optimized, output)

        print(f"Saved: {output} ({size // 1024} KB)")

        manifest.append({
            "id": number,
            "name": uzbek_name,
            "file": filename,
            "status": "ok",
            "title": selected.get("title"),
            "source": selected.get("source"),
            "provider": selected.get("provider"),
            "license": selected.get("license"),
            "license_version": selected.get("license_version"),
            "creator": selected.get("creator"),
            "source_url": selected.get("url"),
            "foreign_landing_url": selected.get("foreign_landing_url"),
            "width": selected.get("width"),
            "height": selected.get("height"),
            "file_size_bytes": size,
        })

        # Be polite to the API.
        time.sleep(1)

    MANIFEST.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    ok = sum(x["status"] == "ok" for x in manifest)
    missing = len(manifest) - ok

    print("\n==============================")
    print(f"READY: {ok}")
    print(f"MISSING/FAILED: {missing}")
    print("==============================")


if __name__ == "__main__":
    main()
