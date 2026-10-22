# 🎨 Chizilgan rasmlar

Ilovadagi rasmlar bolalar ensiklopediyasidagi kabi chizilgan bo‘ladi.
Har bir kategoriya uchun ChatGPT bitta umumiy rasm chizadi: ichida
**6 ta obyekt, 3 ustun × 2 qator**. Keyin bu rasm `scripts/crop_sheets.py`
orqali 6 ta alohida rasmga qirqiladi.

## Qanday ishlaydi

1. Quyidagi promptni ChatGPT’ga **o‘zgartirmasdan** bering (har kategoriya
   alohida). Hammasida uslub matni bir xil, shuning uchun rasmlar ham bir xil
   uslubda chiqadi.
2. Natijani tekshiring: 6 ta obyekt, to‘g‘ri tartibda, yozuvsiz, oq fonda,
   bir-biriga tegmagan. Xato bo‘lsa, qayta chizdiring.
3. Rasmni `art/sheets/` papkasiga jadvaldagi nom bilan qo‘ying
   (`.png`, `.jpg` yoki `.webp`).
4. Qirqish:

   ```bash
   pip install pillow numpy
   python scripts/crop_sheets.py
   ```

   Natija `public/images/` ichiga `01_01_sher.webp` kabi nomlar bilan
   tushadi. Agar skript “teng kataklar (tekshirib ko‘ring!)” desa,
   obyektlar bir-biriga juda yaqin chizilgan bo‘ladi. Qirqilgan rasmlarni
   ko‘z bilan tekshiring.

| Kategoriya | Fayl nomi | Tartib (yuqori qator → pastki qator) |
|---|---|---|
| Yovvoyi hayvonlar | `01_yovvoyi_hayvonlar` | Sher, Fil, Jirafa → Zebra, Maymun, Karkidon |
| Qushlar | `04_qushlar` | Burgut, Boyo‘g‘li, Qarg‘a → Kabutar, Laylak, Qaldirg‘och |
| Mevalar | `06_mevalar` | Olma, Nok, Apelsin → Banan, Uzum, Anor |
| Gullar | `08_gullar` | Atirgul, Lola, Moychechak → Binafsha, Nargiz, Rayhon guli |
| Uy hayvonlari | `10_uy_hayvonlari` | Mushuk, It, Ot → Sigir, Qo‘y, Echki |

Yangi kategoriya qo‘shish uchun `art/sheets.json` ga yangi yozuv va bu yerga
yangi prompt qo‘shiladi.

## Promptlar

### 01 — Yovvoyi hayvonlar

```
Create one landscape image (3:2) with 6 separate illustrations in a neat grid: 3 columns, 2 rows.
Style: classic children's nature encyclopedia illustration — realistic, accurate proportions, hand-painted watercolor with fine colored-pencil details, soft natural colors.
Background: plain pure white everywhere, no paper texture, no scenery, no ground; at most a very light soft shadow under each subject.
Layout: each subject drawn whole, centered in its own cell, all roughly the same size, with wide empty white space between subjects; nothing touches or overlaps.
No text, letters, numbers, labels, captions, signatures, borders, frames or grid lines.
Subjects, full body, side view, standing:
Top row, left to right: adult male lion with a mane, African elephant, giraffe.
Bottom row, left to right: zebra, monkey, rhinoceros.
```

### 04 — Qushlar

```
Create one landscape image (3:2) with 6 separate illustrations in a neat grid: 3 columns, 2 rows.
Style: classic children's nature encyclopedia illustration — realistic, accurate proportions, hand-painted watercolor with fine colored-pencil details, soft natural colors.
Background: plain pure white everywhere, no paper texture, no scenery, no ground; at most a very light soft shadow under each subject.
Layout: each subject drawn whole, centered in its own cell, all roughly the same size, with wide empty white space between subjects; nothing touches or overlaps.
No text, letters, numbers, labels, captions, signatures, borders, frames or grid lines.
Subjects, whole bird, perched or standing with wings folded, no branches:
Top row, left to right: golden eagle, Eurasian eagle-owl, black crow.
Bottom row, left to right: grey rock pigeon, white stork, barn swallow.
```

### 06 — Mevalar

```
Create one landscape image (3:2) with 6 separate illustrations in a neat grid: 3 columns, 2 rows.
Style: classic children's nature encyclopedia illustration — realistic, accurate proportions, hand-painted watercolor with fine colored-pencil details, soft natural colors.
Background: plain pure white everywhere, no paper texture, no scenery, no ground; at most a very light soft shadow under each subject.
Layout: each subject drawn whole, centered in its own cell, all roughly the same size, with wide empty white space between subjects; nothing touches or overlaps.
No text, letters, numbers, labels, captions, signatures, borders, frames or grid lines.
Subjects, one whole fruit per cell, a small leaf where natural, not cut:
Top row, left to right: red apple, yellow-green pear, orange.
Bottom row, left to right: bunch of yellow bananas, bunch of green grapes, pomegranate.
```

### 08 — Gullar

```
Create one landscape image (3:2) with 6 separate illustrations in a neat grid: 3 columns, 2 rows.
Style: classic children's nature encyclopedia illustration — realistic, accurate proportions, hand-painted watercolor with fine colored-pencil details, soft natural colors.
Background: plain pure white everywhere, no paper texture, no scenery, no ground; at most a very light soft shadow under each subject.
Layout: each subject drawn whole, centered in its own cell, all roughly the same size, with wide empty white space between subjects; nothing touches or overlaps.
No text, letters, numbers, labels, captions, signatures, borders, frames or grid lines.
Subjects, a single flower on its stem with leaves, no vase, no pot:
Top row, left to right: red rose, red tulip, chamomile.
Bottom row, left to right: purple sweet violet, yellow daffodil, green basil plant with small white flowers.
```

### 10 — Uy hayvonlari

```
Create one landscape image (3:2) with 6 separate illustrations in a neat grid: 3 columns, 2 rows.
Style: classic children's nature encyclopedia illustration — realistic, accurate proportions, hand-painted watercolor with fine colored-pencil details, soft natural colors.
Background: plain pure white everywhere, no paper texture, no scenery, no ground; at most a very light soft shadow under each subject.
Layout: each subject drawn whole, centered in its own cell, all roughly the same size, with wide empty white space between subjects; nothing touches or overlaps.
No text, letters, numbers, labels, captions, signatures, borders, frames or grid lines.
Subjects, full body, side view, standing:
Top row, left to right: domestic cat, dog, horse.
Bottom row, left to right: cow, sheep, goat.
```
