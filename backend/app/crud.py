# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models
from typing import Optional, List

def get_quiz_by_url(db: Session, url: str) -> Optional[models.QuizRecord]:
    return db.query(models.QuizRecord).filter(models.QuizRecord.url == url).first()

def create_quiz_record(db: Session, item: dict) -> models.QuizRecord:
    rec = models.QuizRecord(
        url = item.get("url"),
        title = item.get("title"),
        summary = item.get("summary"),
        key_entities = item.get("key_entities"),
        sections = item.get("sections"),
        raw_html = item.get("raw_html"),
        quiz_json = item.get("quiz_json")
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

def list_quizzes(db: Session, skip: int = 0, limit: int = 100) -> List[models.QuizRecord]:
    return db.query(models.QuizRecord).order_by(models.QuizRecord.created_at.desc()).offset(skip).limit(limit).all()

def get_quiz(db: Session, quiz_id: int) -> Optional[models.QuizRecord]:
    return db.query(models.QuizRecord).filter(models.QuizRecord.id == quiz_id).first()
