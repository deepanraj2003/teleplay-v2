from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio

from backend.bot_runner import run_bot
from backend.database import engine
from backend.models import Base, Movie
from sqlalchemy.orm import Session

import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")


@app.get("/api/stream/{file_id}")
def stream_video(file_id: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    res = requests.get(url).json()

    file_path = res["result"]["file_path"]

    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    return {"url": file_url}

app = FastAPI()

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ Serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/player")
def player():
    return FileResponse("frontend/player.html")


# ✅ API: Get movies
@app.get("/api/movies")
def get_movies():
    db = Session(bind=engine)
    movies = db.query(Movie).all()
    db.close()

    return [
        {"id": m.id, "name": m.name, "file_id": m.file_id}
        for m in movies
    ]


# ✅ Start bot
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_bot())
