from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import SynthesisRequest, SynthesisResponse
from app.services.synthesizer import synthesize_articles
from app.models.models import BriefingSynthesis

router = APIRouter()

@router.post("/synthesize")
async def synthesize_briefing(
    request: SynthesisRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Generate AI-powered synthesis of multiple articles"""
    # Call synthesis service
    synthesis_result = await synthesize_articles(
        topic=request.topic,
        article_ids=request.article_ids,
        depth=request.depth,
        db=db
    )
    
    # Save to database
    briefing = BriefingSynthesis(
        user_id=user_id,
        topic=request.topic,
        synthesis=synthesis_result['synthesis'],
        source_articles=request.article_ids,
        follow_up_questions=synthesis_result['questions']
    )
    db.add(briefing)
    db.commit()
    db.refresh(briefing)
    
    return {
        "id": briefing.id,
        "topic": briefing.topic,
        "synthesis": briefing.synthesis,
        "follow_up_questions": briefing.follow_up_questions,
        "source_articles": briefing.source_articles
    }

@router.post("/questions")
async def generate_follow_up_questions(topic: str, briefing_id: int):
    """Generate follow-up questions for a briefing"""
    return {
        "briefing_id": briefing_id,
        "questions": [
            "What is the expected market impact?",
            "Which sectors are most affected?",
            "What are the regulatory implications?",
            "Who are the key stakeholders?",
            "What's the timeline for resolution?"
        ]
    }

@router.get("/briefing/{briefing_id}")
async def get_briefing(briefing_id: int, db: Session = Depends(get_db)):
    """Get saved briefing"""
    briefing = db.query(BriefingSynthesis).filter(
        BriefingSynthesis.id == briefing_id
    ).first()
    
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing not found")
    
    return {
        "id": briefing.id,
        "topic": briefing.topic,
        "synthesis": briefing.synthesis,
        "follow_up_questions": briefing.follow_up_questions,
        "source_articles": briefing.source_articles,
        "created_at": briefing.created_at
    }
