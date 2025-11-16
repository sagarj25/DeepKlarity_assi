from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from .db import Base

class QuizRecord(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1024), unique=True, index=True)
    title = Column(String(512))
    summary = Column(Text)
    key_entities = Column(JSON)      # {"people":[], "organizations":[], "locations":[]}
    sections = Column(JSON)          # list of section titles
    raw_html = Column(Text)          # optional — stores raw HTML
    quiz_json = Column(JSON)         # {"quiz": [...], "related_topics": [...]}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
