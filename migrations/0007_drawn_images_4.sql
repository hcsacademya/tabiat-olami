-- Chizilgan rasmlarning to‘rtinchi qismi: Mevalar.

UPDATE items SET image_url = replace(image_url, '.svg', '.webp')
WHERE image_url IN (
  '/images/06_01_olma.svg', '/images/06_02_nok.svg', '/images/06_03_apelsin.svg',
  '/images/06_04_banan.svg', '/images/06_05_uzum.svg', '/images/06_06_anor.svg'
);
