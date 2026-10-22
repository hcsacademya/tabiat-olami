-- Chizilgan rasmlarning ikkinchi qismi: Uy hayvonlari 2.

UPDATE items SET image_url = replace(image_url, '.svg', '.webp')
WHERE image_url IN (
  '/images/10_07_quyon.svg', '/images/10_08_tovuq.svg',
  '/images/10_09_o_rdak.svg', '/images/10_10_eshak.svg'
);

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 10, 'Tuya', 'Tuya haqida qisqa ma’lumot.', '/images/10_11_tuya.webp', 11
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 10 AND name = 'Tuya');

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 10, 'G‘oz', 'G‘oz haqida qisqa ma’lumot.', '/images/10_12_g_oz.webp', 12
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 10 AND name = 'G‘oz');
