from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
import os

from database import SessionLocal, init_db, Quiz
from scraper import scrape_wikipedia
from llm_quiz_generator import get_llm_chain_article_to_quiz

app = FastAPI(title="AI Wiki Quiz Generator", docs_url="/docs")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

generate_quiz_llm = get_llm_chain_article_to_quiz()

@app.get("/")
def home():
    return {"msg": "AI Quiz Generator API running."}

@app.post("/generate_quiz")
def generate_quiz(data: dict):
    url = data.get("url")
    if not url or "wikipedia.org/wiki/" not in url:
        raise HTTPException(status_code=400, detail="Provide a valid Wikipedia article URL.")

    db: Session = SessionLocal()

    # Check for duplicate (cache)
    existing = db.query(Quiz).filter(Quiz.url == url).first()
    if existing:
        quiz_json = json.loads(existing.full_quiz_data)
        quiz_json['id'] = existing.id
        return quiz_json

    # Scrape & clean
    try:
        scraped = scrape_wikipedia(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Scrape error: "+str(e))
    # LLM
    try:
        quiz_json = generate_quiz_llm(scraped["text"], url, scraped["sections"], scraped["summary"])
        quiz_json["title"] = scraped["title"]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Quiz generator error: "+str(e))

    # Store
    try:
        quiz_record = Quiz(
            url=url,
            title=scraped["title"],
            scraped_content=scraped["raw_html"],
            full_quiz_data=json.dumps(quiz_json)
        )
        db.add(quiz_record)
        db.commit()
        db.refresh(quiz_record)
        quiz_json["id"] = quiz_record.id
        return quiz_json
    except Exception as e:
        raise HTTPException(status_code=500, detail="DB error: "+str(e))

@app.get("/history")
def get_history():
    db: Session = SessionLocal()
    quizzes = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
    return [{
        "id": q.id, "url": q.url, "title": q.title,
        "date_generated": q.date_generated.isoformat()
    } for q in quizzes]

@app.get("/quiz/{quiz_id}")
def get_quiz(quiz_id: int):
    db: Session = SessionLocal()
    record = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not found")
    quiz_json = json.loads(record.full_quiz_data)
    quiz_json["id"] = record.id
    return quiz_json
