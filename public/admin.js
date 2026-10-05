let token = localStorage.getItem('tabiat_admin_token') || '';
let cats = [];
let currentItems = [];

const $ = s => document.querySelector(s);

const headers = () => ({
Authorization: 'Bearer ' + token,
'content-type': 'application/json'
});

async function api(url, opt = {}) {
const r = await fetch(url, {
...opt,
headers: {
...headers(),
...(opt.headers || {})
}
});

const d = await r.json().catch(() => ({}));

if (!r.ok) {
throw new Error(d.error || 'Xatolik');
}

return d;
}

function setLogged() {
$('#login').classList.toggle('hidden', !!token);
$('#panel').classList.toggle('hidden', !token);

if (token) {
loadAll();
}
}

async function loadAll() {
cats = await fetch('/api/categories')
.then(r => r.json());

renderCats();

const options = cats.map(c =>
"<option value="${c.id}">${c.icon} ${c.name}</option>"
).join('');

$('#itemCat').innerHTML =
'<option value="">Kategoriyani tanlang</option>' + options;

$('#filterCat').innerHTML =
'<option value="">Kategoriyani tanlang</option>' + options;

if (cats.length) {
$('#itemCat').value = cats[0].id;
$('#filterCat').value = cats[0].id;
loadItems(Number(cats[0].id));
} else {
$('#itemsList').innerHTML =
'<p class="muted">Hozircha kategoriya yo‘q.</p>';
}
}

function renderCats() {
$('#catList').innerHTML = cats.map(c => "<div class="cat-row"> <span>${c.icon} ${c.name}</span> <button class="danger" onclick="delCat(${c.id})"> O‘chirish </button> </div>").join('');
}

async function loadItems(id) {
if (!id) {
$('#itemsList').innerHTML = '';
return;
}

currentItems = await fetch(
'/api/items?category_id=' + id
).then(r => r.json());

$('#itemsList').innerHTML =
currentItems.map(x => `
<div class="item-row">

    <img
      src="${x.image_url || '/default.svg'}"
      alt="${x.name}"
      onerror="this.src='/default.svg'"
    >

    <div class="grow">
      <b>${x.name}</b>
      <div class="muted">
        ${x.description || ''}
      </div>

      ${
        x.image_url
          ? `<div class="muted">${x.image_url}</div>`
          : ''
      }
    </div>

    <button
      class="danger"
      onclick="delItem(${x.id})">
      O‘chirish
    </button>

  </div>
`).join('') ||
'<p class="muted">Hozircha narsa yo‘q.</p>';

}

// =========================
// ADMIN LOGIN
// =========================

$('#loginBtn').onclick = async () => {
try {
const d = await fetch(
'/api/admin/login',
{
method: 'POST',
headers: {
'content-type': 'application/json'
},
body: JSON.stringify({
password: $('#password').value
})
}
).then(r => r.json());

if (!d.token) {
  throw Error(d.error || 'Parol xato');
}

token = d.token;

localStorage.setItem(
  'tabiat_admin_token',
  token
);

$('#password').value = '';

setLogged();

} catch (e) {
$('#loginMsg').textContent = e.message;
}
};

// =========================
// KATEGORIYA QO‘SHISH
// =========================

$('#addCat').onclick = async () => {
try {
const name = $('#catName').value.trim();
const icon = $('#catIcon').value.trim() || '🌿';

if (!name) {
  alert('Kategoriya nomini kiriting');
  return;
}

await api(
  '/api/admin/categories',
  {
    method: 'POST',
    body: JSON.stringify({
      name,
      icon
    })
  }
);

$('#catName').value = '';
$('#catIcon').value = '';

await loadAll();

} catch (e) {
alert(e.message);
}
};

// =========================
// KATEGORIYA O‘CHIRISH
// =========================

window.delCat = async id => {
if (!confirm(
'Kategoriyani va ichidagi narsalarni o‘chirasizmi?'
)) {
return;
}

try {
await api(
'/api/admin/categories?id=' + id,
{
method: 'DELETE'
}
);

await loadAll();

} catch (e) {
alert(e.message);
}
};

// =========================
// KATEGORIYA TANLASH
// =========================

$('#filterCat').onchange = () => {
loadItems(
Number($('#filterCat').value)
);
};

// =========================
// RASM URL BILAN NARSA QO‘SHISH
// =========================

$('#addItem').onclick = async () => {
try {
const categoryId =
Number($('#itemCat').value);

const name =
  $('#itemName').value.trim();

const description =
  $('#itemDesc').value.trim();

const imageUrl =
  $('#itemUrl').value.trim();

if (!categoryId) {
  alert('Avval kategoriyani tanlang');
  return;
}

if (!name) {
  alert('Nomini kiriting');
  return;
}

if (!imageUrl) {
  alert('Rasm URL manzilini kiriting');
  return;
}

await api(
  '/api/admin/items',
  {
    method: 'POST',
    body: JSON.stringify({
      category_id: categoryId,
      name: name,
      description: description,
      image_url: imageUrl
    })
  }
);

$('#itemName').value = '';
$('#itemDesc').value = '';
$('#itemUrl').value = '';

$('#itemMsg').textContent =
  'Saqlandi ✅';

const filterId =
  Number($('#filterCat').value);

if (filterId === categoryId) {
  await loadItems(categoryId);
} else {
  $('#filterCat').value = categoryId;
  await loadItems(categoryId);
}

} catch (e) {
alert(e.message);
}
};

// =========================
// NARSANI O‘CHIRISH
// =========================

window.delItem = async id => {
if (!confirm('O‘chirasizmi?')) {
return;
}

try {
await api(
'/api/admin/items?id=' + id,
{
method: 'DELETE'
}
);

await loadItems(
  Number($('#filterCat').value)
);

} catch (e) {
alert(e.message);
}
};

// =========================
// BOSHLASH
// =========================

setLogged();
