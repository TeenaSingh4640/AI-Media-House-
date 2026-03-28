from sqlalchemy.orm import Session
from app.models.models import Article
from typing import Dict, List
import json

async def synthesize_articles(
    topic: str,
    article_ids: List[int],
    depth: str = "standard",
    db: Session = None
) -> Dict:
    """
    Synthesize multiple articles into a coherent briefing using Claude/LLM
    """
    if db is None:
        from app.database import SessionLocal
        db = SessionLocal()
    
    # Fetch articles
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()
    
    if not articles:
        return {
            "synthesis": "No articles found",
            "questions": []
        }
    
    # Build synthesis prompt
    articles_text = "\n\n".join([
        f"Article: {a.title}\nSource: {a.source}\nContent: {a.content}"
        for a in articles
    ])
    
    # Mock LLM response (replace with actual Claude API call)
    synthesis = await call_llm(topic, articles_text, depth)
    questions = await generate_questions(topic, synthesis)
    
    return {
        "synthesis": synthesis,
        "questions": questions
    }

async def call_llm(topic: str, articles_text: str, depth: str) -> str:
    """
    Call Claude API for synthesis (mock implementation)
    In production, use: from anthropic import Anthropic
    """
    
    depth_instructions = {
        "quick": "Provide a 2-3 sentence summary",
        "standard": "Provide a 150-200 word comprehensive overview",
        "deep": "Provide a detailed 500+ word analysis with all perspectives"
    }
    
    prompt = f"""
    Topic: {topic}
    Depth: {depth_instructions.get(depth, depth_instructions['standard'])}
    
    Based on these articles, create a unified briefing:
    
    {articles_text}
    
    Synthesis:
    """
    
    # Mock response
    mock_synthesis = f"""
    **{topic} - Executive Briefing**
    
    The latest developments in {topic} show significant market movement. Multiple sources indicate 
    substantial changes in the sector, with implications for investors, startups, and market observers.
    
    Key developments:
    • Market dynamics are shifting rapidly
    • Multiple stakeholders are affected
    • Forward-looking implications are significant
    
    This represents a major moment in the {topic} space, with ripple effects expected across related sectors.
    """
    
    return mock_synthesis

async def generate_questions(topic: str, synthesis: str) -> List[str]:
    """
    Generate follow-up questions based on synthesis
    """
    return [
        f"What is the regulatory impact of this {topic} development?",
        f"Which companies are most affected by this {topic} change?",
        f"How does this affect the competitive landscape in {topic}?",
        f"What are the investment implications of this {topic} news?",
        f"What should stakeholders watch for next in {topic}?"
    ]
