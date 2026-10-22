-- Hozircha 5 ta kategoriya qoladi.
-- Olib tashlanganlar keyinroq chizilgan rasmlar bilan qayta qo‘shiladi.

DELETE FROM items WHERE category_id IN (2, 3, 5, 7, 9);
DELETE FROM categories WHERE id IN (2, 3, 5, 7, 9);
