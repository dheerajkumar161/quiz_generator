from pydantic import BaseModel
from typing import List, Dict, Optional

class KeyEntities(BaseModel):
    people: List[str] = []
    organizations: List[str] = []
    locations: List[str] = []

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

class QuizOutput(BaseModel):
    id: Optional[int]
    url: str
    title: str
    summary: str
    key_entities: KeyEntities
    sections: List[str]
    quiz: List[QuizQuestion]
    related_topics: List[str]
