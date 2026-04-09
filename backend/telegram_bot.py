from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from backend.database import SessionLocal
from backend.models import Movie

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")


# ✅ Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot working 🚀")


# ✅ Save uploaded video
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.document

    if not video:
        return

    file_id = video.file_id
    name = video.file_name or "Unknown Movie"

    db = SessionLocal()
    movie = Movie(name=name, file_id=file_id)
    db.add(movie)
    db.commit()
    db.close()

    await update.message.reply_text(f"Saved: {name}")


def create_application():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", start))
    app.add_handler(
        CommandHandler("help", start)
    )

    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, handle_video))

    return app
