import threading
from telegram_bot import start_bot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from models import Movie

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "TelePlay v2 is running 🚀"}


# 🔥 ADD MOVIE (TEST)
@app.get("/add-test")
def add_test_movie():
    db = SessionLocal()

    movie = Movie(
        name="Test Movie",
        file_id="123456"
    )

    db.add(movie)
    db.commit()
    db.close()

    return {"message": "Test movie added"}


# 🔥 GET ALL MOVIES
@app.get("/movies")
def get_movies():
    db = SessionLocal()
    movies = db.query(Movie).all()
    db.close()

    return movies
# Start bot in background
threading.Thread(target=start_bot).start()
