-- Chizilgan rasmlarning birinchi qismi (art/sheets dan qirqilgan).

UPDATE items SET image_url = replace(image_url, '.svg', '.webp')
WHERE image_url IN (
  '/images/01_01_sher.svg', '/images/01_02_fil.svg', '/images/01_03_jirafa.svg',
  '/images/01_04_zebra.svg', '/images/01_05_maymun.svg', '/images/01_06_karkidon.svg',
  '/images/01_07_begemot.svg', '/images/01_08_kiyik.svg', '/images/01_09_gorilla.svg',
  '/images/01_10_kenguru.svg',
  '/images/04_01_burgut.svg', '/images/04_02_boyo_g_li.svg', '/images/04_03_qarg_a.svg',
  '/images/04_04_kabutar.svg', '/images/04_05_laylak.svg', '/images/04_06_qaldirg_och.svg',
  '/images/08_01_atirgul.svg', '/images/08_02_lola.svg', '/images/08_03_moychechak.svg',
  '/images/08_04_binafsha.svg', '/images/08_05_nargiz.svg', '/images/08_06_rayhon_guli.svg',
  '/images/10_01_mushuk.svg', '/images/10_02_it.svg', '/images/10_03_ot.svg',
  '/images/10_04_sigir.svg', '/images/10_05_qo_y.svg', '/images/10_06_echki.svg'
);

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 1, 'Olmaxon', 'Olmaxon haqida qisqa ma’lumot.', '/images/01_11_olmaxon.webp', 11
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 1 AND name = 'Olmaxon');

INSERT INTO items(category_id, name, description, image_url, sort_order)
SELECT 1, 'Tipratikan', 'Tipratikan haqida qisqa ma’lumot.', '/images/01_12_tipratikan.webp', 12
WHERE NOT EXISTS (SELECT 1 FROM items WHERE category_id = 1 AND name = 'Tipratikan');
