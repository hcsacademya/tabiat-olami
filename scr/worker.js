const json = (data, status = 200) => new Response(JSON.stringify(data), {
status,
headers: {
'content-type': 'application/json; charset=utf-8',
'cache-control': 'no-store'
}
});

function corsHeaders() {
return {
'access-control-allow-origin': '*',
'access-control-allow-methods': 'GET,POST,PUT,DELETE,OPTIONS',
'access-control-allow-headers': 'content-type, authorization'
};
}

function withCors(response) {
const headers = new Headers(response.headers);
Object.entries(corsHeaders()).forEach(([k, v]) => headers.set(k, v));
return new Response(response.body, {
status: response.status,
headers
});
}

async function telegram(env, method, body) {
const r = await fetch(
"https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/${method}",
{
method: 'POST',
headers: { 'content-type': 'application/json' },
body: JSON.stringify(body)
}
);

return r.json();
}

function token() {
return crypto.randomUUID().replaceAll('-', '') +
crypto.randomUUID().replaceAll('-', '');
}

async function requireAdmin(request, env) {
const auth = request.headers.get('authorization') || '';
const value = auth.startsWith('Bearer ') ? auth.slice(7) : '';

if (!value) return false;

const row = await env.DB
.prepare(
'SELECT token FROM sessions WHERE token = ? AND expires_at > ?'
)
.bind(value, Date.now())
.first();

return !!row;
}

async function serveAsset(request, env) {
return env.ASSETS.fetch(request);
}

export default {
async fetch(request, env) {
if (request.method === 'OPTIONS') {
return new Response(null, { headers: corsHeaders() });
}

const url = new URL(request.url);
const path = url.pathname;

try {
  // =========================
  // TELEGRAM WEBHOOK
  // =========================

  if (
    path === '/telegram/webhook' &&
    request.method === 'POST'
  ) {
    const secret =
      request.headers.get(
        'x-telegram-bot-api-secret-token'
      );

    if (
      !env.TELEGRAM_WEBHOOK_SECRET ||
      secret !== env.TELEGRAM_WEBHOOK_SECRET
    ) {
      return new Response('Forbidden', { status: 403 });
    }

    const update = await request.json();
    const msg = update.message;

    if (msg?.chat?.id) {
      const chatId = msg.chat.id;
      const text = msg.text || '';
      const appUrl = env.PUBLIC_APP_URL;

      if (text.startsWith('/start') || text === '/app') {
        await telegram(env, 'sendMessage', {
          chat_id: chatId,
          text:
            '🌿 Tabiat Olami\n\n' +
            'Hayvonlar, qushlar, baliqlar, mevalar va o‘simliklarni ' +
            'rasmlar orqali o‘rganing.',
          reply_markup: {
            inline_keyboard: [[
              {
                text: '🌿 Mini Appni ochish',
                web_app: { url: appUrl }
              }
            ]]
          }
        });
      } else {
        await telegram(env, 'sendMessage', {
          chat_id: chatId,
          text:
            'Mini Appni ochish uchun quyidagi tugmani bosing:',
          reply_markup: {
            inline_keyboard: [[
              {
                text: '🌿 Mini Appni ochish',
                web_app: { url: appUrl }
              }
            ]]
          }
        });
      }
    }

    return new Response('OK');
  }

  // =========================
  // PUBLIC API
  // =========================

  if (
    path === '/api/categories' &&
    request.method === 'GET'
  ) {
    const rows = await env.DB
      .prepare(
        'SELECT id, name, icon FROM categories ' +
        'ORDER BY sort_order, id'
      )
      .all();

    return withCors(
      json(rows.results || [])
    );
  }

  if (
    path === '/api/items' &&
    request.method === 'GET'
  ) {
    const categoryId =
      Number(url.searchParams.get('category_id'));

    if (!categoryId) {
      return withCors(
        json({ error: 'category_id kerak' }, 400)
      );
    }

    const rows = await env.DB
      .prepare(
        'SELECT id, category_id, name, description, image_url ' +
        'FROM items ' +
        'WHERE category_id = ? ' +
        'ORDER BY sort_order, id'
      )
      .bind(categoryId)
      .all();

    return withCors(
      json(rows.results || [])
    );
  }

  // =========================
  // ADMIN LOGIN
  // =========================

  if (
    path === '/api/admin/login' &&
    request.method === 'POST'
  ) {
    const body = await request.json();

    if (
      !env.ADMIN_PASSWORD ||
      body.password !== env.ADMIN_PASSWORD
    ) {
      return withCors(
        json({ error: 'Parol noto‘g‘ri' }, 401)
      );
    }

    const t = token();
    const expires =
      Date.now() + 1000 * 60 * 60 * 24 * 7;

    await env.DB
      .prepare(
        'INSERT INTO sessions(token, created_at, expires_at) ' +
        'VALUES (?, ?, ?)'
      )
      .bind(t, Date.now(), expires)
      .run();

    return withCors(
      json({
        token: t,
        expires_at: expires
      })
    );
  }

  // =========================
  // ADMIN CATEGORIES
  // =========================

  if (
    path === '/api/admin/categories' &&
    request.method === 'POST'
  ) {
    if (!await requireAdmin(request, env)) {
      return withCors(
        json({ error: 'Ruxsat yo‘q' }, 401)
      );
    }

    const b = await request.json();

    if (!b.name) {
      return withCors(
        json({ error: 'Kategoriya nomi kerak' }, 400)
      );
    }

    const max = await env.DB
      .prepare(
        'SELECT COALESCE(MAX(sort_order), 0) AS m ' +
        'FROM categories'
      )
      .first();

    const r = await env.DB
      .prepare(
        'INSERT INTO categories(name, icon, sort_order) ' +
        'VALUES (?, ?, ?)'
      )
      .bind(
        b.name,
        b.icon || '🌿',
        Number(max?.m || 0) + 1
      )
      .run();

    return withCors(
      json({ id: r.meta.last_row_id })
    );
  }

  if (
    path === '/api/admin/categories' &&
    request.method === 'DELETE'
  ) {
    if (!await requireAdmin(request, env)) {
      return withCors(
        json({ error: 'Ruxsat yo‘q' }, 401)
      );
    }

    const id =
      Number(url.searchParams.get('id'));

    await env.DB
      .prepare(
        'DELETE FROM categories WHERE id = ?'
      )
      .bind(id)
      .run();

    return withCors(
      json({ ok: true })
    );
  }

  // =========================
  // ADMIN ITEMS - ADD
  // =========================

  if (
    path === '/api/admin/items' &&
    request.method === 'POST'
  ) {
    if (!await requireAdmin(request, env)) {
      return withCors(
        json({ error: 'Ruxsat yo‘q' }, 401)
      );
    }

    const b = await request.json();

    if (!b.category_id || !b.name) {
      return withCors(
        json({
          error: 'Kategoriya va nom kerak'
        }, 400)
      );
    }

    const max = await env.DB
      .prepare(
        'SELECT COALESCE(MAX(sort_order), 0) AS m ' +
        'FROM items WHERE category_id = ?'
      )
      .bind(Number(b.category_id))
      .first();

    const r = await env.DB
      .prepare(
        'INSERT INTO items(' +
        'category_id, name, description, image_url, sort_order' +
        ') VALUES (?, ?, ?, ?, ?)'
      )
      .bind(
        Number(b.category_id),
        b.name,
        b.description || '',
        b.image_url || '',
        Number(max?.m || 0) + 1
      )
      .run();

    return withCors(
      json({ id: r.meta.last_row_id })
    );
  }

  // =========================
  // ADMIN ITEMS - EDIT
  // =========================

  if (
    path === '/api/admin/items' &&
    request.method === 'PUT'
  ) {
    if (!await requireAdmin(request, env)) {
      return withCors(
        json({ error: 'Ruxsat yo‘q' }, 401)
      );
    }

    const b = await request.json();

    if (!b.id || !b.category_id || !b.name) {
      return withCors(
        json({
          error: 'Ma’lumotlar to‘liq emas'
        }, 400)
      );
    }

    await env.DB
      .prepare(
        'UPDATE items SET ' +
        'category_id=?, name=?, description=?, image_url=? ' +
        'WHERE id=?'
      )
      .bind(
        Number(b.category_id),
        b.name,
        b.description || '',
        b.image_url || '',
        Number(b.id)
      )
      .run();

    return withCors(
      json({ ok: true })
    );
  }

  // =========================
  // ADMIN ITEMS - DELETE
  // =========================

  if (
    path === '/api/admin/items' &&
    request.method === 'DELETE'
  ) {
    if (!await requireAdmin(request, env)) {
      return withCors(
        json({ error: 'Ruxsat yo‘q' }, 401)
      );
    }

    const id =
      Number(url.searchParams.get('id'));

    await env.DB
      .prepare(
        'DELETE FROM items WHERE id=?'
      )
      .bind(id)
      .run();

    return withCors(
      json({ ok: true })
    );
  }

  // =========================
  // R2 OLIB TASHLANDI
  // =========================
  //
  // Rasm fayli endi Worker orqali yuklanmaydi.
  // Admin panel image_url maydoniga rasmning
  // internetdagi to‘liq URL manzilini yuboradi.
  //
  // Masalan:
  // https://example.com/sher.jpg
  //
  // =========================

  if (
    path === '/api/admin/upload' &&
    request.method === 'POST'
  ) {
    if (!await requireAdmin(request, env)) {
      return withCors(
        json({ error: 'Rasm yuklash funksiyasi R2siz o‘chirildi' }, 410)
      );
    }

    return withCors(
      json({
        error:
          'R2 ishlatilmaydi. Rasm URL manzilini image_url orqali kiriting.'
      }, 410)
    );
  }

  // =========================
  // STATIC ASSETS
  // =========================

  return serveAsset(request, env);

} catch (e) {
  console.error(e);

  if (path.startsWith('/api/')) {
    return withCors(
      json({
        error: 'Server xatosi',
        detail: String(e?.message || e)
      }, 500)
    );
  }

  return new Response(
    'Server xatosi',
    { status: 500 }
  );
}

}
};
