from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserProfileCreate(BaseModel):
    email: str
    name: str
    profile_type: str  # "investor", "founder", "student"
    interests: dict

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    profile_type: Optional[str] = None
    interests: Optional[dict] = None
    preferences: Optional[dict] = None

class ArticleCreate(BaseModel):
    title: str
    url: str
    source: str
    content: str
    published_at: datetime
    tags: List[str]

class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    summary: Optional[str]
    sentiment: Optional[float]
    tags: List[str]
    published_at: datetime
    
    class Config:
        from_attributes = True

class FeedResponse(BaseModel):
    articles: List[ArticleResponse]
    total: int

class SynthesisRequest(BaseModel):
    topic: str
    article_ids: List[int]
    depth: str = "standard"  # "quick", "standard", "deep"

class SynthesisResponse(BaseModel):
    synthesis: str
    follow_up_questions: List[str]
    source_articles: List[int]
