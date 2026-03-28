from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Article
from app.schemas.schemas import ArticleCreate
from app.services.article_processor import process_article_async
from datetime import datetime

router = APIRouter()

@router.post("/ingest")
async def ingest_article(
    article: ArticleCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Ingest a new article - process in background"""
    # Check if article already exists
    existing = db.query(Article).filter(Article.url == article.url).first()
    if existing:
        return {"message": "Article already processed", "article_id": existing.id}
    
    # Create article record
    db_article = Article(
        title=article.title,
        url=article.url,
        source=article.source,
        content=article.content,
        published_at=article.published_at,
        tags=article.tags,
        summary="Processing...",
        sentiment=0.0
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    # Queue background processing
    background_tasks.add_task(process_article_async, db_article.id)
    
    return {
        "article_id": db_article.id,
        "title": db_article.title,
        "status": "processing"
    }

@router.get("/{article_id}")
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get article details"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return {
        "id": article.id,
        "title": article.title,
        "url": article.url,
        "source": article.source,
        "content": article.content,
        "summary": article.summary,
        "sentiment": article.sentiment,
        "tags": article.tags,
        "entities": article.entities,
        "published_at": article.published_at
    }

@router.post("/search")
async def search_articles(query: str, limit: int = 10, db: Session = Depends(get_db)):
    """Search articles by keyword"""
    articles = db.query(Article).filter(
        Article.title.ilike(f"%{query}%") |
        Article.content.ilike(f"%{query}%")
    ).limit(limit).all()
    
    return {
        "query": query,
        "count": len(articles),
        "articles": [
            {
                "id": a.id,
                "title": a.title,
                "url": a.url,
                "source": a.source,
                "sentiment": a.sentiment,
                "published_at": a.published_at
            }
            for a in articles
        ]
    }
