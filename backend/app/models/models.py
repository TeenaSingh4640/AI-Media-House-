from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, Enum, JSON
from datetime import datetime
import enum
from app.database import Base

# ============================================================================
# USER & AUTHENTICATION MODELS
# ============================================================================

class UserProfile(Base):
    """Enhanced user profile with behavioral tracking and preference learning"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    profile_type = Column(String)  # "investor", "founder", "student", "general"
    
    # Interests & Preferences
    interests = Column(JSON, default={})  # {sectors: [], companies: [], topics: [], regions: []}
    preferences = Column(JSON, default={})  # {alert_frequency, summary_length, channels}
    expertise_level = Column(String, default="beginner")  # beginner/intermediate/advanced (auto-detected)
    
    # Behavioral Data
    viewed_articles = Column(JSON, default=[])  # [article_ids]
    saved_articles = Column(JSON, default=[])  # [article_ids]
    engagement_time = Column(Integer, default=0)  # Total minutes
    interaction_history = Column(JSON, default=[])  # Recent interactions for context
    
    # Profile Stats
    recommendation_feedback = Column(JSON, default={})  # {article_id: rating}
    topic_affinity = Column(JSON, default={})  # {topic: score}
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)


class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    token = Column(String, unique=True)
    device_info = Column(JSON, default={})  # Browser, OS, device type
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


# ============================================================================
# ARTICLE & NLP MODELS
# ============================================================================

class Article(Base):
    """Enhanced article model with NLP, embeddings, and real-time metrics"""
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    source = Column(String, index=True)  # "ET", "Reuters", etc
    author = Column(String, nullable=True)
    content = Column(Text)
    summary = Column(Text)  # Auto-generated
    
    # Publishing & Ingestion Metadata
    published_at = Column(DateTime, index=True)
    ingested_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # NLP Results
    sentiment = Column(Float, default=0.0)  # -1 to 1 (bearish to bullish)
    sentiment_details = Column(JSON, default={})  # {confidence, aspect_sentiments}
    entities = Column(JSON, default={})  # {companies: [], people: [], sectors: [], products: []}
    topics = Column(JSON, default=[])  # [topic_name, confidence, ...]
    keywords = Column(JSON, default=[])  # [keyword, keyword, ...]
    
    # Semantic Vector (stored as string, actual vector in Pinecone)
    vector_id = Column(String, nullable=True)  # Pinecone/Weaviate vector ID
    semantic_signature = Column(String, nullable=True)  # Hash for deduplication
    
    # Real-time Metrics
    view_count = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)  # Derived from views, saves, shares
    click_through_rate = Column(Float, default=0.0)
    
    # Classification
    article_type = Column(String)  # "breaking", "trending", "analysis", "news"
    is_breaking = Column(Boolean, default=False)
    trend_score = Column(Float, default=0.0)  # Part of trend (0-1)
    
    # Multimodal
    has_image = Column(Boolean, default=False)
    image_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    
    # Status
    is_archived = Column(Boolean, default=False)
    related_articles = Column(JSON, default=[])  # [article_ids]


class Entity(Base):
    """Knowledge graph entities (companies, people, sectors, etc.)"""
    __tablename__ = "entities"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_name = Column(String, unique=True, index=True)
    entity_type = Column(String, index=True)  # company, person, sector, product, location
    
    # Entity Properties
    description = Column(Text, nullable=True)
    entity_metadata = Column(JSON, default={})  # domain, ticker, sector, etc.
    
    # Mention Tracking
    mention_count = Column(Integer, default=0)
    last_mentioned = Column(DateTime, default=datetime.utcnow)
    trend_velocity = Column(Float, default=0.0)  # Mentions per hour
    
    # Sentiment Tracking
    avg_sentiment = Column(Float, default=0.0)
    sentiment_trend = Column(Float, default=0.0)  # Positive or negative trend
    
    # Related Entities
    related_entities = Column(JSON, default=[])  # [entity_id, relation_type, ...]
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# TREND & PREDICTION MODELS
# ============================================================================

class Trend(Base):
    """Real-time trending stories and entities"""
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, index=True)  # References Entity.id
    entity_name = Column(String, index=True)
    entity_type = Column(String)  # company, sector, topic
    
    # Trend Velocity
    hourly_mentions = Column(Integer, default=0)
    mention_velocity = Column(Float, default=0.0)  # Acceleration of mentions
    
    # Engagement Metrics
    total_engagement = Column(Float, default=0.0)
    engagement_trend = Column(Float, default=0.0)  # Positive or negative
    
    # Sentiment Dynamics
    sentiment_average = Column(Float, default=0.0)
    sentiment_change = Column(Float, default=0.0)  # 1h change
    
    # Rank & Classification
    trend_rank = Column(Integer)  # Current position in trending list
    trend_score = Column(Float, default=0.0)  # 0-100
    is_emerging = Column(Boolean, default=False)  # Breaking trend
    is_sustained = Column(Boolean, default=False)  # Multi-day trend
    
    # Related Articles & Context
    top_articles = Column(JSON, default=[])  # [article_ids]
    related_entities = Column(JSON, default=[])  # [entity_ids]
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow)
    trend_start = Column(DateTime)
    predicted_end = Column(DateTime, nullable=True)


class Prediction(Base):
    """Trend and story predictions"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, nullable=True)  # NULL for story predictions
    entity_name = Column(String, nullable=True)
    prediction_type = Column(String)  # "emerging_story", "sector_momentum", "impact_scenario"
    
    # Prediction Details
    title = Column(String)
    description = Column(Text)
    confidence_score = Column(Float)  # 0-1
    
    # Temporal
    predicted_timeframe = Column(String)  # "48h", "72h", "1w"
    impact_potential = Column(String)  # "low", "medium", "high", "critical"
    
    # Supporting Data
    correlations = Column(JSON, default=[])  # Correlated entities/topics
    historical_patterns = Column(JSON, default=[])  # Similar past events
    evidence_articles = Column(JSON, default=[])  # Supporting articles
    
    # Status & Tracking
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Did prediction materialize?
    
    created_at = Column(DateTime, default=datetime.utcnow)
    predicted_date = Column(DateTime)
    verified_at = Column(DateTime, nullable=True)


# ============================================================================
# FEED & INTERACTION MODELS
# ============================================================================

class UserFeed(Base):
    """Personalized feed generation"""
    __tablename__ = "user_feeds"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    article_id = Column(Integer)
    
    # Ranking & Scoring
    relevance_score = Column(Float)  # Why relevant to this user (0-1)
    rank = Column(Integer)  # Position in feed
    
    # Personalization Details
    personalization_reason = Column(String)  # "sector_interest", "trending", "similar_read"
    recommendation_source = Column(String)  # "collaborative", "content_based", "trending"
    
    # Interaction Tracking
    viewed = Column(Boolean, default=False)
    view_time = Column(Integer, default=0)  # Seconds
    saved = Column(Boolean, default=False)
    shared = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    viewed_at = Column(DateTime, nullable=True)


class NewsEvent(Base):
    """Major news events with timeline and entity mapping"""
    __tablename__ = "news_events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    
    # Event Timeline
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, nullable=True)
    predicted_duration = Column(String, nullable=True)  # "1-2 weeks", "1-3 months"
    
    # Content & Coverage
    key_articles = Column(JSON, default=[])  # [article_ids in chronological order]
    article_count = Column(Integer, default=0)
    
    # Entity Mapping
    key_entities = Column(JSON, default={})  # {company: [], person: [], sector: []}
    entity_roles = Column(JSON, default={})  # {entity_id: role}
    
    # Event Progression
    timeline = Column(JSON, default=[])  # [{date, milestone, sentiment, entities}]
    
    # Impact Assessment
    impact_score = Column(Float, default=0.0)
    affected_sectors = Column(JSON, default=[])
    affected_companies = Column(JSON, default=[])
    
    # Status
    event_status = Column(String, default="ongoing")  # ongoing, resolved, archived
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class BriefingSynthesis(Base):
    """RAG-based synthesis and Q&A results"""
    __tablename__ = "briefing_syntheses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    query = Column(String)  # Original user question
    
    # Synthesis Content
    synthesis = Column(Text)  # Generated response
    summary_level = Column(String)  # tweet, brief, detailed
    
    # Source Attribution
    source_articles = Column(JSON, default=[])  # [{article_id, citation_text, relevance}]
    sources_cited = Column(Integer, default=0)
    
    # AI Generation Details
    follow_up_questions = Column(JSON, default=[])  # Auto-generated questions
    confidence_score = Column(Float, default=0.0)
    
    # Caching & Performance
    cache_key = Column(String, nullable=True)
    is_cached = Column(Boolean, default=False)
    cache_ttl = Column(Integer, default=1800)  # 30 minutes
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
class ConversationContext(Base):
    """Multi-turn conversation context for chat"""
    __tablename__ = "conversation_contexts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    session_id = Column(String, index=True)
    
    # Conversation History
    messages = Column(JSON, default=[])  # [{role, content, timestamp}]
    
    # Context
    current_topic = Column(String, nullable=True)
    entities_in_context = Column(JSON, default=[])
    sentiment_context = Column(String, nullable=True)
    
    # Performance
    message_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # Auto-cleanup old sessions


# ============================================================================
# CACHING & PERFORMANCE MODELS
# ============================================================================

class VectorCache(Base):
    """Cache for frequently accessed embeddings"""
    __tablename__ = "vector_caches"
    
    id = Column(Integer, primary_key=True, index=True)
    query_hash = Column(String, unique=True, index=True)
    query = Column(String)
    
    # Results
    vector_results = Column(JSON, default=[])  # [{article_id, similarity_score}]
    result_count = Column(Integer, default=0)
    
    # Cache Management
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    ttl = Column(Integer, default=86400)  # 24 hours


class AIResponseCache(Base):
    """Cache for LLM responses to reduce cost"""
    __tablename__ = "ai_response_caches"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_hash = Column(String, unique=True, index=True)
    prompt = Column(String)
    
    # Response
    response = Column(Text)
    response_tokens = Column(Integer, default=0)
    
    # Cost & Performance
    cost_saved = Column(Float, default=0.0)
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    ttl = Column(Integer, default=1800)  # 30 minutes
