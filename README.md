# 🌿 Tabiat Olami — Telegram Mini App

Oddiy va sodda Telegram Mini App: kategoriya → 10 ta obyekt → rasm → o‘zbekcha nom → 🔊 Eshitish.

Admin panel orqali kategoriya va rasmlarni qo‘shish/o‘chirish mumkin. Rasm R2 ga yuklanadi. Ovoz brauzer/telefonning `SpeechSynthesis` imkoniyati orqali `uz-UZ` sifatida so‘raladi; mavjud ovozlar qurilmaga qarab farq qilishi mumkin.

## Tarkib

- `public/` — Mini App va Admin panel
- `src/worker.js` — Cloudflare Worker API + Telegram webhook
- `migrations/` — D1 database schema va boshlang‘ich 100 ta obyekt
- `wrangler.toml` — Cloudflare konfiguratsiyasi

## 1. GitHub

Bu papkani GitHub repository'ga yuklang.

## 2. Cloudflare resurslari

Cloudflare'da:

1. **D1 Database** yarating: `tabiat-db`
2. **R2 Bucket** yarating: `tabiat-images`
3. `wrangler.toml` ichidagi `REPLACE_WITH_YOUR_D1_DATABASE_ID` o‘rniga D1 ID ni yozing.
4. `PUBLIC_APP_URL` ni keyin chiqadigan Mini App domeningizga almashtiring.

Agar Wrangler ishlatsangiz:

```bash
npm install
npx wrangler d1 create tabiat-db
npx wrangler r2 bucket create tabiat-images
```

Keyin D1 ID ni `wrangler.toml`ga qo‘ying.

## 3. D1 bazani to‘ldirish

```bash
npx wrangler d1 migrations apply tabiat-db --remote
```

Bu schema bilan birga boshlang‘ich **10 kategoriya × 10 ta = 100 ta** obyektni yaratadi. Boshlang‘ich rasmlar demo SVG ko‘rinishida. Haqiqiy rasmlarni Admin paneldan almashtirib/qo‘shib borasiz.

## 4. Admin parolini berish

```bash
npx wrangler secret put ADMIN_PASSWORD
```

Masalan kuchli parol kiriting.

## 5. Telegram Bot tokeni

BotFather orqali bot yarating va tokenni:

```bash
npx wrangler secret put TELEGRAM_BOT_TOKEN
```

orqali saqlang.

Webhook xavfsizlik kaliti:

```bash
npx wrangler secret put TELEGRAM_WEBHOOK_SECRET
```

Masalan: uzun tasodifiy satr.

## 6. Cloudflare'ga deploy

```bash
npm run deploy
```

Deploydan keyin sizga Worker URL beradi, masalan:

`https://tabiat-olami-mini-app.<subdomain>.workers.dev`

Shuni `wrangler.toml`dagi `PUBLIC_APP_URL` qiymatiga yozib, yana deploy qiling.

## 7. Telegram webhook ulash

Brauzer yoki terminaldan quyidagiga o‘xshash so‘rov yuboring:

```text
https://api.telegram.org/botBOT_TOKEN/setWebhook?url=https://YOUR-WORKER-DOMAIN/telegram/webhook&secret_token=YOUR_WEBHOOK_SECRET
```

`BOT_TOKEN`, domen va `YOUR_WEBHOOK_SECRET`ni o‘zingiznikiga almashtiring.

Botga `/start` yozilganda **🌿 Mini Appni ochish** tugmasi chiqadi.

## 8. Admin panel

Deploydan keyin:

`https://YOUR-WORKER-DOMAIN/admin.html`

Manziliga kiring va `ADMIN_PASSWORD` bilan kiring.

Admin panelda:

- kategoriya qo‘shish;
- nom yozish;
- rasm yuklash;
- rasm URL berish;
- qisqa ma’lumot yozish;
- obyektni o‘chirish

mumkin.

## GitHub → Cloudflare avtomatik deploy

Cloudflare Dashboard → **Workers & Pages** → **Create** → Git repository bilan ulash. Build command kerak emas; Worker deploy qilinadi.

Agar Cloudflare interfeysida GitHub deploy sozlamalari boshqa ko‘rinishda chiqsa, repository sifatida shu loyihani tanlab `npm run deploy` emas, Cloudflare'ning Worker build/deploy integratsiyasini yoqing. Eng ishonchli variant — avval lokal `npx wrangler deploy` bilan tekshirish, keyin Git integration'ni ulash.

## Muhim

Bu loyiha ataylab sodda qilingan: React/Vue kabi katta frontend framework yo‘q. Oddiy HTML/CSS/JS + Cloudflare Worker + D1 + R2 ishlatiladi.
