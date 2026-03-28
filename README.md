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


