import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from database import SessionLocal
from models import Movie

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        message = update.channel_post

        if message.video or message.document:
            file = message.video or message.document

            db = SessionLocal()

            movie = Movie(
                name=file.file_name or "Unknown",
                file_id=file.file_id
            )

            db.add(movie)
            db.commit()
            db.close()

            print(f"Saved: {file.file_name}")


def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, handle_files))

    print("Bot started...")
    app.run_polling()
