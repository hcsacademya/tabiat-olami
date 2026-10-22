-- Chizilgan rasmlarning uchinchi qismi: Qushlar 2, Mevalar 2, Gullar 2.

UPDATE items SET image_url = replace(image_url, '.svg', '.webp')
WHERE image_url IN (
  '/images/04_07_to_tiqush.svg', '/images/04_08_tovus.svg',
  '/images/04_09_oqqush.svg', '/images/04_10_flamingo.svg',
  '/images/06_07_shaftoli.svg', '/images/06_08_gilos.svg',
  '/images/06_09_qulupnay.svg', '/images/06_10_mango.svg',
  '/images/08_07_boychechak.svg', '/images/08_08_orxideya.svg',
  '/images/08_09_kungaboqar.svg', '/images/08_10_chinnigul.svg'
);

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 4, 'Chumchuq', 'Chumchuq haqida qisqa ma’lumot.', '/images/04_11_chumchuq.webp', 11
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 4 AND name = 'Chumchuq');

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 4, 'Pingvin', 'Pingvin haqida qisqa ma’lumot.', '/images/04_12_pingvin.webp', 12
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 4 AND name = 'Pingvin');

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 6, 'O‘rik', 'O‘rik haqida qisqa ma’lumot.', '/images/06_11_o_rik.webp', 11
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 6 AND name = 'O‘rik');

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 6, 'Limon', 'Limon haqida qisqa ma’lumot.', '/images/06_12_limon.webp', 12
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 6 AND name = 'Limon');

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 8, 'Qoqio‘t', 'Qoqio‘t haqida qisqa ma’lumot.', '/images/08_11_qoqio_t.webp', 11
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 8 AND name = 'Qoqio‘t');

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 8, 'Lolaqizg‘aldoq', 'Lolaqizg‘aldoq haqida qisqa ma’lumot.', '/images/08_12_lolaqizg_aldoq.webp', 12
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 8 AND name = 'Lolaqizg‘aldoq');
