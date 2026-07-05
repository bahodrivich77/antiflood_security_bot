import asyncio
import json
import re

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import TOKEN
from antiflood import flood
from admin import handlers
from database import init_db
from keepalive import start_keepalive

with open("blacklist.json", encoding="utf8") as f:
    _raw_blacklist = json.load(f)

LINK = re.compile(
    r"(https?://|t\.me/|telegram\.me/|@\w+)",
    re.I
)

# Reklamachilar so'z ichiga ko'zga ko'rinmas belgilar (zero-width,
# invisible Unicode) qo'shib filtrlardan qochishga harakat qiladi.
# Tekshirishdan oldin bunday belgilarni va apostroflarni tozalaymiz.
INVISIBLE_CHARS = re.compile(
    r"[\u200b\u200c\u200d\u200e\u200f\ufeff\u2060-\u2064\u206a-\u206f]"
)
APOSTROPHES = re.compile(r"[\'\u2018\u2019\u02bc\u02bb`]")


def normalize(text: str) -> str:
    text = INVISIBLE_CHARS.sub("", text)
    text = APOSTROPHES.sub("", text)
    return text.lower()


BLACKLIST = [normalize(word) for word in _raw_blacklist]


async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if update.effective_chat.type == "private":
        return

    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )

    if member.status in ["administrator", "creator"]:
        return

    text = normalize(
        update.message.text
        or update.message.caption
        or ""
    )

    # 1) Flood tekshiruvi (10 soniyada 5 tadan ortiq xabar)
    if await flood(update.effective_user.id):
        await update.message.delete()
        try:
            await context.bot.restrict_chat_member(
                update.effective_chat.id,
                update.effective_user.id,
                permissions={}
            )
        except Exception:
            pass
        return

    # 2) Link/reklama tekshiruvi
    if LINK.search(text):
        await update.message.delete()
        try:
            await context.bot.ban_chat_member(
                update.effective_chat.id,
                update.effective_user.id
            )
        except Exception:
            pass
        return

    # 3) Qora ro'yxat so'zlari
    for word in BLACKLIST:
        if word in text:
            await update.message.delete()
            try:
                await context.bot.ban_chat_member(
                    update.effective_chat.id,
                    update.effective_user.id
                )
            except Exception:
                pass
            return


async def post_init(application: Application):
    await init_db()


def main():
    # Render "Web Service" bir portni tinglashini kutadi, aks holda
    # xizmatni o'chirib qo'yadi. Shu uchun kichik HTTP server ochamiz.
    start_keepalive()

    # Python 3.13+/3.14: asosiy thread'da endi avtomatik event loop
    # yaratilmaydi, shuning uchun uni o'zimiz qo'lda o'rnatamiz.
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(
        MessageHandler(filters.ALL, spam)
    )

    for h in handlers:
        app.add_handler(h)

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()