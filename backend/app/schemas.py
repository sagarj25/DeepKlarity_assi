from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

# Request Model
class GenerateRequest(BaseModel):
    url: HttpUrl


# Quiz Question Schema
class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str
    difficulty: str


# Main Output Schema
class QuizRecordOut(BaseModel):
    id: int
    url: str
    title: Optional[str]
    summary: Optional[str]
    key_entities: Optional[Dict[str, List[str]]]
    sections: Optional[List[str]]
    quiz: Optional[List[QuizQuestion]]
    related_topics: Optional[List[str]]
    created_at: Optional[str]

    class Config:
        orm_mode = True
