from sqlalchemy.orm import Session
from app.models.models import Article, UserFeed, UserProfile
from typing import List
import json

async def process_article_async(article_id: int, db: Session = None):
    """
    Process article: summarize, extract entities, vectorize, and distribute to feeds
    Placeholder for real ML pipeline
    """
    if db is None:
        from app.database import SessionLocal
        db = SessionLocal()
    
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return
    
    # Mock processing
    article.summary = f"Summary of {article.title}: {article.content[:200]}..."
    article.sentiment = 0.5  # Mock sentiment
    article.entities = {
        "companies": ["TCS", "Infosys", "Wipro"],
        "sectors": ["IT", "Finance"],
        "people": ["CEO Name"]
    }
    
    # Vectorize and store (mock)
    article.vector_id = f"vec_{article.id}"
    
    db.commit()
    
    # Distribute to user feeds based on profile
    await distribute_to_feeds(article_id, db)

async def distribute_to_feeds(article_id: int, db: Session):
    """
    Distribute article to relevant user feeds based on interests
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return
    
    # Get all users
    users = db.query(UserProfile).all()
    
    for user in users:
        # Calculate relevance score based on interests
        relevance_score = calculate_relevance(article, user)
        
        if relevance_score > 0.3:  # Threshold
            feed_item = UserFeed(
                user_id=user.id,
                article_id=article_id,
                relevance_score=relevance_score,
                personalization_reason=get_personalization_reason(article, user)
            )
            db.add(feed_item)
    
    db.commit()

def calculate_relevance(article, user) -> float:
    """
    Calculate relevance score (0-1) between article and user profile
    """
    score = 0.0
    
    if not user.interests:
        return 0.5  # Default score
    
    # Check sector interests
    if "sectors" in user.interests and article.entities:
        user_sectors = user.interests.get("sectors", [])
        article_sectors = article.entities.get("sectors", [])
        sector_matches = len(set(user_sectors) & set(article_sectors))
        score += min(sector_matches * 0.2, 0.4)
    
    # Check company interests
    if "companies" in user.interests and article.entities:
        user_companies = user.interests.get("companies", [])
        article_companies = article.entities.get("companies", [])
        company_matches = len(set(user_companies) & set(article_companies))
        score += min(company_matches * 0.25, 0.4)
    
    # Profile-specific boost
    if user.profile_type == "investor" and article.sentiment > 0:
        score += 0.1
    elif user.profile_type == "founder" and "startup" in article.title.lower():
        score += 0.15
    elif user.profile_type == "student" and len(article.summary) > 0:
        score += 0.05
    
    return min(score, 1.0)

def get_personalization_reason(article, user) -> str:
    """Get reason why article was recommended"""
    reasons = []
    
    if user.interests and article.entities:
        user_sectors = user.interests.get("sectors", [])
        article_sectors = article.entities.get("sectors", [])
        if set(user_sectors) & set(article_sectors):
            reasons.append("Matches your sector interests")
        
        user_companies = user.interests.get("companies", [])
        article_companies = article.entities.get("companies", [])
        if set(user_companies) & set(article_companies):
            reasons.append("Mentions your followed companies")
    
    if user.profile_type == "investor":
        reasons.append("Relevant to investor profile")
    elif user.profile_type == "founder":
        reasons.append("Startup news")
    
    return " • ".join(reasons) if reasons else "Trending topic"
