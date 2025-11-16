# backend/app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import HttpUrl
import traceback

from . import db, models, schemas, utils, crud, llm_client
from .db import engine

# Create DB tables (simple approach)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DeepKlarity Quiz Generator API")

# Allow frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate_quiz", response_model=schemas.QuizRecordOut)
def generate_quiz(payload: schemas.GenerateRequest, db_session: Session = Depends(db.get_db)):
    url = payload.url
    if not utils.is_wikipedia_url(url):
        raise HTTPException(status_code=400, detail="URL must be a Wikipedia URL")

    # caching: return existing record if found
    existing = crud.get_quiz_by_url(db_session, url)
    if existing:
        return {
            "id": existing.id,
            "url": existing.url,
            "title": existing.title,
            "summary": existing.summary,
            "key_entities": existing.key_entities,
            "sections": existing.sections,
            "quiz": existing.quiz_json.get("quiz", []),
            "related_topics": existing.quiz_json.get("related_topics", []),
            "created_at": existing.created_at.isoformat()
        }

    # fetch page
    try:
        html = utils.fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

    parsed = utils.extract_wikipedia_content(html)
    title = parsed.get("title") or url
    article_text = parsed.get("full_text", "")

    if len(article_text.strip()) < 50:
        raise HTTPException(status_code=422, detail="Article content too short to generate quiz")

    # generate via LLM
    try:
        llm_out = llm_client.generate_quiz_and_topics(title=title, article_text=article_text)
    except Exception as e:
        # include traceback in server logs; return user-friendly message
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="LLM generation failed. Check server logs for details.")

    rec_obj = {
        "url": url,
        "title": title,
        "summary": parsed.get("summary"),
        "key_entities": parsed.get("key_entities", {}),
        "sections": parsed.get("sections", []),
        "raw_html": html,
        "quiz_json": {
            "quiz": llm_out.get("quiz", []),
            "related_topics": llm_out.get("related_topics", [])
        }
    }

    created = crud.create_quiz_record(db_session, rec_obj)

    return {
        "id": created.id,
        "url": created.url,
        "title": created.title,
        "summary": created.summary,
        "key_entities": created.key_entities,
        "sections": created.sections,
        "quiz": created.quiz_json.get("quiz", []),
        "related_topics": created.quiz_json.get("related_topics", []),
        "created_at": created.created_at.isoformat()
    }

@app.get("/api/quizzes", response_model=list[schemas.QuizRecordOut])
def list_quiz(db_session: Session = Depends(db.get_db)):
    items = crud.list_quizzes(db_session)
    out = []
    for i in items:
        out.append({
            "id": i.id,
            "url": i.url,
            "title": i.title,
            "summary": i.summary,
            "key_entities": i.key_entities,
            "sections": i.sections,
            "quiz": i.quiz_json.get("quiz", []),
            "related_topics": i.quiz_json.get("related_topics", []),
            "created_at": i.created_at.isoformat()
        })
    return out

@app.get("/api/quizzes/{quiz_id}", response_model=schemas.QuizRecordOut)
def get_quiz(quiz_id: int, db_session: Session = Depends(db.get_db)):
    rec = crud.get_quiz(db_session, quiz_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {
        "id": rec.id,
        "url": rec.url,
        "title": rec.title,
        "summary": rec.summary,
        "key_entities": rec.key_entities,
        "sections": rec.sections,
        "quiz": rec.quiz_json.get("quiz", []),
        "related_topics": rec.quiz_json.get("related_topics", []),
        "created_at": rec.created_at.isoformat()
    }
