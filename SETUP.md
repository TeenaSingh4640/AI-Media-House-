# AI-Native News Platform - Setup Instructions

## Project Overview

This is a full-stack AI-powered business news platform with personalized newsrooms, AI synthesis of articles, and interactive briefings.

**Architecture:**
- Frontend: Next.js 14 + React + TypeScript
- Backend: FastAPI + Python 3.11
- Database: PostgreSQL + Redis
- Vector DB: Pinecone (for semantic search)
- AI/LLM: Claude API via LangChain

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose (optional)

### Option 1: Using Docker (Recommended)

```bash
# Copy environment file
cp .env.example .env

# Fill in your API keys in .env
# - CLAUDE_API_KEY
# - OPENAI_API_KEY
# - PINECONE_API_KEY

# Start all services
docker-compose up
```

Visit:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL and Redis locally
# Then run:
python app/main.py
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

## Key Features Implemented

### 1. My ET (Personalized Newsroom)
- User profile-based personalization (investor/founder/student)
- Interest-driven content filtering
- Relevance scoring algorithm
- Distributed feed generation

**Location:** [backend/app/api/feed.py](backend/app/api/feed.py)

### 2. News Navigator (AI Synthesis)
- Multi-article synthesis via LLM
- Follow-up question generation
- Depth-based summarization (quick/standard/deep)
- Source article tracking

**Location:** [backend/app/api/navigator.py](backend/app/api/navigator.py)

### 3. User Profiling System
- Multi-faceted profile types
- Interest management (sectors, companies, topics)
- Preferences customization
- Dynamic profile updates

**Location:** [backend/app/api/profiles.py](backend/app/api/profiles.py)

### 4. Article Processing Pipeline
- Async article ingestion
- Automatic summarization
- Entity extraction
- Sentiment analysis
- Vectorization for semantic search

**Location:** [backend/app/services/article_processor.py](backend/app/services/article_processor.py)

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile/{user_id}` - Get user profile

### Feed
- `GET /api/feed/personalized?user_id={id}` - Get personalized feed
- `GET /api/feed/trending` - Get trending articles

### Articles
- `POST /api/articles/ingest` - Ingest new article
- `GET /api/articles/{article_id}` - Get article details
- `POST /api/articles/search` - Search articles

### Navigator
- `POST /api/navigator/synthesize` - Generate synthesis
- `POST /api/navigator/questions` - Get follow-up questions
- `GET /api/navigator/briefing/{briefing_id}` - Get saved briefing

### Profiles
- `PUT /api/profiles/{user_id}` - Update user profile
- `POST /api/profiles/{user_id}/interests` - Add interests

## Database Schema

**User Profiles:**
- id, email, name, profile_type, interests, preferences, timestamps

**Articles:**
- id, title, url, source, content, summary, sentiment, entities, tags, vector_id

**News Events:**
- id, title, description, start_date, end_date, related_articles, timeline

**User Feeds:**
- id, user_id, article_id, relevance_score, personalization_reason

**Briefing Synthesis:**
- id, user_id, topic, synthesis, source_articles, follow_up_questions

## Frontend Pages

- `/` - Login/Signup with profile selection
- `/feed` - Personalized news feed
- `/navigator` - AI synthesis briefings
- `/profile` - Profile customization

## Next Steps for Production

1. **Replace Mock LLM:** Update [backend/app/services/synthesizer.py](backend/app/services/synthesizer.py) to use real Claude API
2. **Vector Database Integration:** Implement Pinecone semantic search in article_processor
3. **Authentication:** Upgrade from simplified token to JWT with refresh tokens
4. **News Ingestion:** Add real news sources (ET API, NewsAPI, etc.)
5. **Video Generation:** Implement AI video studio using Remotion + ElevenLabs
6. **Entity Extraction:** Add NER models for companies, people, sectors
7. **Sentiment Analysis:** Integrate transformer models for sentiment scoring
8. **Story Arc Tracking:** Build knowledge graph and timeline visualization
9. **Caching:** Implement Redis caching for feeds and syntheses
10. **Monitoring:** Add logging and error tracking

## Environment Variables

See [.env.example](.env.example) for all required environment variables.

Key API keys needed:
- Claude API key from Anthropic
- OpenAI API key (optional)
- Pinecone API key for vector search

## Troubleshooting

1. **Database connection error:** Ensure PostgreSQL is running and DATABASE_URL is correct
2. **API not responding:** Check backend is running on port 8000
3. **Frontend won't load:** Verify NEXT_PUBLIC_API_URL is set correctly
4. **Cold start on first request:** Backend performs initial model loading

## Development Workflow

```bash
# Terminal 1: Backend
cd backend
python app/main.py

# Terminal 2: Frontend  
cd frontend
npm run dev

# Access at http://localhost:3000
```

## Testing

Add articles via API:
```bash
curl -X POST http://localhost:8000/api/articles/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Article",
    "url": "https://example.com/article",
    "source": "ET",
    "content": "Lorem ipsum dolor sit amet...",
    "published_at": "2024-01-15T10:00:00",
    "tags": ["technology", "startup"]
  }'
```

Get personalized feed:
```bash
curl http://localhost:8000/api/feed/personalized?user_id=1
```

## Support & Resources

- FastAPI Docs: http://localhost:8000/docs
- Next.js Docs: https://nextjs.org/docs
- Pydantic: https://docs.pydantic.dev
- SQLAlchemy: https://docs.sqlalchemy.org
