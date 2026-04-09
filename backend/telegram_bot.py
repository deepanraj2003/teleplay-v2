from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import *

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Application.builder().token(BOT_TOKEN).build()


# ✅ Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a movie 🎬")


# ✅ Handle video upload
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video

    if not video:
        return

    file_id = video.file_id
    name = video.file_name or "Unknown"

    db: Session = SessionLocal()

    movie = Movie(name=name, file_id=file_id)
    db.add(movie)
    db.commit()
    db.close()

    await update.message.reply_text(f"Saved: {name} ✅")


# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO, handle_video))


# ✅ RUN BOT (IMPORTANT FIX)
async def run_bot():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("Bot started...")

    # keep running forever
    await app.updater.idle()
