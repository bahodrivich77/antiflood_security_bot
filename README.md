# Telegram Anti-Spam Bot

## O'rnatish (Windows)

1. Python 3.10+ o'rnatilganiga ishonch hosil qiling.
2. Loyiha papkasida terminal (CMD/PowerShell) oching va kutubxonalarni o'rnating:

   ```
   pip install -r requirements.txt
   ```

3. `.env.example` faylini `.env` deb nomlang va o'z BOT_TOKEN'ingizni yozing:

   ```
   BOT_TOKEN=123456:ABCDEF...
   LOG_CHAT_ID=
   ```

   Tokenni @BotFather orqali olasiz.

4. Botni guruhingizga qo'shing va **Administrator** qilib, quyidagi huquqlarni bering:
   - Delete messages
   - Ban users
   - Restrict members
   - Read messages (default)

5. Botni ishga tushiring:

   ```
   python bot.py
   ```

## Fayllar tuzilishi

- `bot.py` — asosiy fayl, botni ishga tushiradi.
- `config.py` — .env fayldan sozlamalarni o'qiydi.
- `blacklist.json` — taqiqlangan so'zlar/iboralar ro'yxati (kerak bo'lsa qo'shib/olib tashlang).
- `database.py` — SQLite orqali warn (ogohlantirish) tizimini saqlaydi.
- `antiflood.py` — 10 soniyada 5 tadan ortiq xabar yuborgan foydalanuvchini aniqlaydi.
- `admin.py` — admin buyruqlari: `/warn`, `/ban`, `/unban`, `/mute`, `/unmute`.

## Bot nima qiladi

- Link/reklama (`http://`, `https://`, `t.me/`, `@username`) yuborilsa — xabarni o'chiradi va foydalanuvchini ban qiladi.
- `blacklist.json` dagi so'zlardan biri yozilsa — xabarni o'chiradi va ban qiladi.
- 10 soniya ichida 5 tadan ortiq xabar yuborilsa — flood deb hisoblanadi, xabar o'chiriladi va foydalanuvchi restrict qilinadi.
- Adminlar va guruh egasi tekshiruvlardan ozod (ular reklama/link yuborishi mumkin).
- `/warn` — xabarga reply qilib yozilsa, foydalanuvchiga ogohlantirish beriladi; 3-ogohlantirishda avtomatik ban qilinadi.
- `/ban`, `/unban`, `/mute`, `/unmute` — admin buyruqlari (reply qilib ishlatiladi, `/unban` esa user_id bilan: `/unban 123456789`).

## Render'ga joylash (bepul, 24/7 uchun "uxlamasin" hiylasi bilan)

Render'ning bepul tarifida "Background Worker" yo'q, faqat "Web Service" bepul — u esa 15 daqiqa hech kim so'rov yubormasa uxlab qoladi. Shu sababli botga kichik HTTP server (`keepalive.py`) qo'shilgan — Render buni "web service" deb tanib, o'chirib qo'ymaydi. Botni doim uyg'oq tutish uchun tashqi "pinger" xizmati (masalan UptimeRobot) kerak bo'ladi.

### 1-qadam — Kodni GitHub'ga yuklash

1. [github.com](https://github.com)'da yangi **private** repository yarating (masalan `telegram-antispam-bot`).
2. `.env` faylini **hech qachon** GitHub'ga yuklamang (`.gitignore` allaqachon shuni ta'minlaydi).
3. Loyiha papkasida:
   ```
   git init
   git add .
   git commit -m "Birinchi joylash"
   git branch -M main
   git remote add origin https://github.com/FOYDALANUVCHI_NOMI/telegram-antispam-bot.git
   git push -u origin main
   ```

### 2-qadam — Render'da servis yaratish

1. [render.com](https://render.com)'da ro'yxatdan o'ting va GitHub hisobingizni ulang.
2. **New → Web Service** tanlang, repositoryingizni tanlang.
3. Sozlamalar:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** Free
4. **Environment** bo'limida quyidagi o'zgaruvchilarni qo'shing (`.env` fayldagidek):
   - `BOT_TOKEN` = tokeningiz
   - `LOG_CHAT_ID` = (agar kerak bo'lsa)
5. **Create Web Service** tugmasini bosing. Build tugagach, bot ishga tushadi va sizga `https://sizning-bot-nomi.onrender.com` manzilini beradi.
6. Brauzerda shu manzilni ochib, "Bot ishlab turibdi ✅" degan matn chiqsa — hammasi to'g'ri ishlayapti.

### 3-qadam — Botni uxlatib qo'ymaslik (UptimeRobot)

1. [uptimerobot.com](https://uptimerobot.com)'da bepul hisob ochish.
2. **Add New Monitor** → Monitor Type: `HTTP(s)` → URL: Render bergan manzil (masalan `https://sizning-bot-nomi.onrender.com`).
3. **Monitoring Interval**: 5 daqiqa qilib qo'ying.

Shundan keyin UptimeRobot har 5 daqiqada shu manzilga so'rov yuborib turadi, Render esa buni "faoliyat bor" deb hisoblab, xizmatni uxlatmaydi.

**Eslatma:** bu — bepul, ammo 100% kafolatlanmagan usul (Render ba'zan qisqa vaqtga qayta ishga tushirib qo'yishi mumkin, shu daqiqada bot bir necha soniya javob bermay qolishi mumkin). To'liq ishonchli, uzluksiz ishlash kerak bo'lsa, Render'ning pullik Background Worker tarifi ($7/oy) yoki Oracle Cloud Free Tier'dagi doimiy server tavsiya etiladi.


## Qo'shimcha eslatma

- Bu bot hozircha oddiy kalit so'z va regex asosida ishlaydi (AI orqali aniqlash, captcha, raid-protection kabi imkoniyatlar hali qo'shilmagan). Kerak bo'lsa keyingi bosqichda qo'shib beriladi.
- `blacklist.json` ni o'zingizga mos ravishda kengaytirishingiz mumkin — bu oddiy JSON massiv.
