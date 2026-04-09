from fastapi import FastAPI
import asyncio
from backend.telegram_bot import run_bot

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API running"}


# ✅ Correct startup (NO LOOP CONFLICT)
@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
