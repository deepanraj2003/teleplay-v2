import asyncio
from backend.telegram_bot import create_application


async def run_bot():
    app = create_application()

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("Bot started...")

    await asyncio.Event().wait()
