# AI-Native News Platform

A next-generation business news experience powered by AI - personalized newsrooms, interactive briefings, automated video generation, and story tracking.

## Features

### MVP Phase
- **My ET** - Personalized newsroom tailored to user profile (investor/founder/student)
- **News Navigator** - AI-powered synthesis of related articles with interactive Q&A
- **News Ingestion** - Real-time article fetching and vectorization
- **User Profiling** - Profile-based content personalization

### Future Features
- **AI Video Studio** - Auto-generate broadcast-quality news videos
- **Story Arc Tracker** - Interactive timelines with entity mapping and sentiment tracking
- **Vernacular Engine** - Context-aware translation to Hindi, Tamil, Telugu, Bengali

## Tech Stack

- **Frontend**: Next.js 14 + React + TypeScript
- **Backend**: FastAPI + Python 3.11
- **Database**: PostgreSQL
- **Vector DB**: Pinecone/Weaviate for semantic search
- **AI/LLM**: Claude API via LangChain
- **Deployment**: Vercel (frontend) + Railway/AWS (backend)

## Project Structure

```
├── frontend/          # Next.js React app
├── backend/           # FastAPI Python server
├── shared/            # Shared types and utilities
├── .github/           # GitHub workflows and docs
└── docker-compose.yml # Local development setup
```

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Environment Variables

Create `.env.local` in `frontend/` and `.env` in `backend/`:

**Frontend:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_KEY=your_api_key
```

**Backend:**
```
DATABASE_URL=postgresql://user:password@localhost:5432/ai_news
REDIS_URL=redis://localhost:6379
CLAUDE_API_KEY=your_claude_key
PINECONE_API_KEY=your_pinecone_key
```

## API Endpoints

- `POST /api/auth/signup` - Register user
- `POST /api/auth/login` - Login
- `GET /api/feed/personalized` - Get personalized news feed
- `POST /api/articles/process` - Ingest and vectorize article
- `POST /api/navigator/synthesize` - Get AI synthesis of articles
- `GET /api/navigator/questions` - Generate follow-up questions
- `POST /api/profiles/update` - Update user profile

## Development

### Run Full Stack Locally
```bash
docker-compose up
npm run dev --workspace=frontend
```

### Database Migrations
```bash
cd backend
alembic upgrade head
```

### Check Linting
```bash
cd frontend && npm run lint
cd backend && flake8 . && black --check .
```

## Deployment

**Frontend** (Vercel):
```bash
npm run build
npm run deploy
```

**Backend** (Railway/AWS):
```bash
cd backend
docker build -t ai-news-backend .
```

## License

MIT
