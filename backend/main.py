from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio

from backend.bot_runner import run_bot
from backend.database import engine
from backend.models import Base, Movie
from sqlalchemy.orm import Session

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
