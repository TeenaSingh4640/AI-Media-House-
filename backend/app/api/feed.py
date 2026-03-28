from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models.models import Article, UserFeed, UserProfile
from app.schemas.schemas import FeedResponse, ArticleResponse
from typing import List

router = APIRouter()

@router.get("/personalized")
async def get_personalized_feed(user_id: int, limit: int = 20, db: Session = Depends(get_db)):
    """Get personalized feed for user based on profile"""
    # Get user profile
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's feed
    feed_items = db.query(UserFeed).filter(
        UserFeed.user_id == user_id
    ).order_by(
        desc(UserFeed.relevance_score)
    ).limit(limit).all()
    
    # Get full article details
    article_ids = [item.article_id for item in feed_items]
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()
    
    articles_data = [
        ArticleResponse(
            id=a.id,
            title=a.title,
            url=a.url,
            summary=a.summary,
            sentiment=a.sentiment,
            tags=a.tags,
            published_at=a.published_at
        )
        for a in articles
    ]
    
    return {
        "articles": articles_data,
        "total": len(articles_data),
        "profile_type": user.profile_type
    }

@router.get("/trending")
async def get_trending_feed(limit: int = 10, db: Session = Depends(get_db)):
    """Get trending articles across all users"""
    articles = db.query(Article).order_by(
        desc(Article.published_at)
    ).limit(limit).all()
    
    articles_data = [
        ArticleResponse(
            id=a.id,
            title=a.title,
            url=a.url,
            summary=a.summary,
            sentiment=a.sentiment,
            tags=a.tags,
            published_at=a.published_at
        )
        for a in articles
    ]
    
    return {
        "articles": articles_data,
        "total": len(articles_data)
    }
