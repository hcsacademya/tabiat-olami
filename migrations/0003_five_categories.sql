-- Hozircha 5 ta kategoriya va har birida 6 tadan obyekt qoladi.
-- Olib tashlanganlar keyinroq chizilgan rasmlar bilan qayta qo‘shiladi.

DELETE FROM items WHERE category_id IN (2, 3, 5, 7, 9);
DELETE FROM categories WHERE id IN (2, 3, 5, 7, 9);

DELETE FROM items WHERE category_id = 1 AND name IN ('Begemot', 'Kiyik', 'Gorilla', 'Kenguru');
DELETE FROM items WHERE category_id = 4 AND name IN ('To‘tiqush', 'Tovus', 'Oqqush', 'Flamingo');
DELETE FROM items WHERE category_id = 6 AND name IN ('Shaftoli', 'Gilos', 'Qulupnay', 'Mango');
DELETE FROM items WHERE category_id = 8 AND name IN ('Boychechak', 'Orxideya', 'Kungaboqar', 'Chinnigul');
DELETE FROM items WHERE category_id = 10 AND name IN ('Quyon', 'Tovuq', 'O‘rdak', 'Eshak');
