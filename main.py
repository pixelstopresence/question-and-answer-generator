from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import random

app = FastAPI(title="Interview AI API")

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later we can lock to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("data.json", "r") as f:
    DATA = json.load(f)


@app.get("/")
def home():
    return {"status": "Interview AI API running 🚀"}


@app.get("/generate")
def generate_questions(
    category: str = Query(...),
    level: str = Query(...),
    count: int = Query(1)
):
    category = category.lower()
    level = level.lower()

    if category not in DATA:
        return {"error": "Invalid category"}

    filtered = [q for q in DATA[category] if q["level"] == level]

    if not filtered:
        return {"error": "No questions found"}

    random.shuffle(filtered)

    return {
        "category": category,
        "level": level,
        "questions": filtered[:count]
    }
