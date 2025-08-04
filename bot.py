import os
import asyncio
from pyrogram import Client
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Env vars
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
SESSION = os.getenv("SESSION", "your_string_session")

# Initialize userbot
userbot = Client(name="escrow_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Escrow Bot Ready!\nSend /escrow to create a private escrow group.")

async def escrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await update.message.reply_text("❌ Use this command in my DM only!")
        return

    user = update.effective_user
    group_title = f"Escrow - {user.first_name}"

    try:
        # Create group & invite link using pyrogram
        new_group = await userbot.create_group(group_title, [user.id])
        invite_link = await userbot.export_chat_invite_link(new_group.id)

        await update.message.reply_text(
            f"**Escrow Group Created** ✅\n"
            f"Creator: {user.mention_html()}\n\n"
            f"Join this escrow group and share the link with the buyer/seller.\n\n"
            f"[Join Group]({invite_link})\n\n"
            f"⚠ Note: Link is valid for 2 members only!",
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to create group: {e}")

# --- Main ---
async def main():
    await userbot.start()
    print("✅ Userbot started!")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("escrow", escrow))

    print("🤖 Escrow Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
