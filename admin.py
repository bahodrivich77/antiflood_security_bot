from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from database import add_warn, get_warn


async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Iltimos, ogohlantirmoqchi bo'lgan foydalanuvchining xabariga javob (reply) qilib /warn yozing."
        )
        return

    uid = update.message.reply_to_message.from_user.id

    await add_warn(uid)
    warns = await get_warn(uid)

    await update.message.reply_text(f"⚠ Warn: {warns}/3")

    if warns >= 3:
        await context.bot.ban_chat_member(
            update.effective_chat.id,
            uid
        )
        await update.message.reply_text("⛔ User banned.")


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Iltimos, ban qilmoqchi bo'lgan foydalanuvchining xabariga javob qilib /ban yozing."
        )
        return

    uid = update.message.reply_to_message.from_user.id
    await context.bot.ban_chat_member(update.effective_chat.id, uid)
    await update.message.reply_text("⛔ Foydalanuvchi ban qilindi.")


async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Foydalanish: /unban <user_id>")
        return

    uid = int(context.args[0])
    await context.bot.unban_chat_member(update.effective_chat.id, uid)
    await update.message.reply_text("✅ Foydalanuvchi unban qilindi.")


async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Iltimos, mute qilmoqchi bo'lgan foydalanuvchining xabariga javob qilib /mute yozing."
        )
        return

    uid = update.message.reply_to_message.from_user.id
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        uid,
        permissions=None
    )
    await update.message.reply_text("🔇 Foydalanuvchi mute qilindi.")


async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Iltimos, unmute qilmoqchi bo'lgan foydalanuvchining xabariga javob qilib /unmute yozing."
        )
        return

    from telegram import ChatPermissions

    uid = update.message.reply_to_message.from_user.id
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        uid,
        permissions=ChatPermissions(can_send_messages=True)
    )
    await update.message.reply_text("🔊 Foydalanuvchi unmute qilindi.")


handlers = [
    CommandHandler("warn", warn),
    CommandHandler("ban", ban),
    CommandHandler("unban", unban),
    CommandHandler("mute", mute),
    CommandHandler("unmute", unmute),
]
