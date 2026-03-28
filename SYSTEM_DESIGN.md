# AI News OS - System Design Document

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  Web Browser (Next.js)         Mobile App              API Clients          │
│  http://localhost:3000         (Future)                (Partners)           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                       API GATEWAY & LOAD BALANCER                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Rate Limiting (100 req/min)    • Request Validation                      │
│  • CORS Handling                   • Authentication                         │
│  • Request Routing                 • Response Compression                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND SERVICES                               │
├────────────────────────────────────────────────────────────────────────────┬┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ AUTH SERVICE          │ USER SERVICE         │ FEED SERVICE          │  │
│  │ ├─ Signup/Login       │ ├─ Profile Mgmt     │ ├─ Feed Generation    │  │
│  │ ├─ Session Mgmt       │ ├─ Preferences      │ ├─ Personalization    │  │
│  │ ├─ JWT Tokens         │ └─ Expertise Level  │ └─ User Feedback      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ SEARCH SERVICE              │ RAG SERVICE           │ TREND SERVICE  │  │
│  │ ├─ Semantic Search          │ ├─ Synthesis         │ ├─ Trending    │  │
│  │ ├─ Hybrid Search (BM25+Vec) │ ├─ Q&A Chat          │ ├─ Predictions │  │
│  │ ├─ Vector Retrieval         │ ├─ Citation          │ └─ Entity Graph│  │
│  │ └─ Reranking                │ └─ Fact Verification │                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ ASYNC SERVICES (Celery Workers)                                     │  │
│  │ ├─ NLP Pipeline (Entity, Sentiment, Topics)                         │  │
│  │ ├─ Article Ingestion & Deduplication                                │  │
│  │ ├─ Embedding Generation                                             │  │
│  │ ├─ Trend Detection & Analysis                                       │  │
│  │ ├─ Recommendation Computation                                       │  │
│  │ └─ Batch Processing                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATA & INTELLIGENCE LAYER                                │
├────────────────────────────┬───────────────────────────┬────────────────────┤
│                            │                           │                    │
│  ┌─────────────────────┐   │  ┌──────────────────┐    │  ┌─────────────┐   │
│  │  PostgreSQL         │   │  │  Redis Cache     │    │  │  Pinecone   │   │
│  │  (Primary DB)       │   │  │  (Hot Cache)     │    │  │  (Vectors)  │   │
│  │                     │   │  │                  │    │  │             │   │
│  │  • Articles         │   │  │  • Sessions      │    │  │  Articles   │   │
│  │  • Users            │   │  │  • User Cache    │    │  │  Search     │   │
│  │  • Entities         │   │  │  • Search Cache  │    │  │  Results    │   │
│  │  • Trends           │   │  │  • LLM Cache     │    │  │ (1.5M Items)│   │
│  │  • Predictions      │   │  │  • Trending      │    │  │             │   │
│  │  • Events           │   │  │                  │    │  │ Sub-100ms   │   │
│  │                     │   │  │  TTL: 1800-3600s │    │  │  Search     │   │
│  │  Replicated         │   │  │                  │    │  │             │   │
│  │  Partitioned        │   │  │  Multi-instance  │    │  │  Replicated │   │
│  │  24h Backup         │   │  │  HA Config       │    │  │  Global     │   │
│  └─────────────────────┘   │  └──────────────────┘    │  └─────────────┘   │
│                            │                           │                    │
└────────────────────────────┴───────────────────────────┴────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES & APIs                                 │
├─────────┬──────────────────┬─────────────────┬──────────────────┬───────────┤
│         │                  │                 │                  │           │
│ OpenAI/ │ News Sources     │ Vector Service  │ Observability    │ Storage   │
│ Claude  │                  │                 │                  │           │
│         │ • Reuters API    │ • Pinecone      │ • Prometheus     │ • S3      │
│ LLM     │ • NewsAPI        │ • Weaviate      │ • Grafana        │ • CDN     │
│ API     │ • Twitter API    │ • OpenSearch    │ • DataDog        │           │
│         │ • RSS Feeds      │                 │ • Sentry         │           │
│         │ • Web Scraping   │                 │                  │           │
│         │                  │                 │                  │           │
└─────────┴──────────────────┴─────────────────┴──────────────────┴───────────┘
```

---

## 📊 Data Flow Diagrams

### 1. News Ingestion Pipeline

```
News Sources (APIs, RSS, Web)
         ↓
    [Ingestion Queue - Kafka/RabbitMQ]
         ↓
    [Article Fetch & Validate]
         ↓
    [Deduplication Engine]
         ├─ Hash-based matching
         └─ Semantic similarity check
         ↓
    [Article Store - PostgreSQL]
         ↓
    [Async NLP Workers]
         ├─ Entity Recognition
         ├─ Sentiment Analysis
         ├─ Topic Extraction
         └─ Summarization
         ↓
    [Update Article with NLP Results]
         ↓
    [Generate Embeddings]
         ├─ Text embeddings (1536-dim)
         └─ Store in vector DB
         ↓
    [Update Search Indices]
         ├─ PostgreSQL full-text index
         ├─ Pinecone vector index
         └─ Redis cache
         ↓
    [Trigger Recommendations]
         ├─ Update trending data
         ├─ Notify similar users
         └─ Update feed rankings
         ↓
    REAL-TIME FEED UPDATES
```

### 2. Personalized Feed Generation

```
User Request (GET /api/feed/personalized)
         ↓
    [Load User Profile]
         ├─ Interests: sectors, companies, topics
         ├─ Preferences: alert_frequency, summary_length
         ├─ Engagement history
         └─ Expertise level
         ↓
    ┌─────────────────────────────────────────┐
    │ RECOMMENDATION ALGORITHMS                │
    │                                          │
    │ 1. Collaborative Filter (40%)            │
    │    ├─ Find similar users                 │
    │    └─ Recommend their liked articles    │
    │                                          │
    │ 2. Content-Based Filter (35%)            │
    │    ├─ Match user interests               │
    │    └─ Score by relevance                 │
    │                                          │
    │ 3. Trending Ranker (25%)                 │
    │    ├─ Global trending topics             │
    │    └─ Filter by user interests           │
    └─────────────────────────────────────────┘
         ↓
    [Merge & Weight Scores]
         ├─ Normalize scores 0-1
         ├─ Apply user preferences
         └─ Consider recency
         ↓
    [Diversity Optimization]
         ├─ Prevent filter bubbles
         ├─ Mix sectors & topics
         └─ Include unexpected reads
         ↓
    [Add Explanations]
         ├─ "Trending in your interest areas"
         ├─ "Similar users liked this"
         └─ "Related to Tesla"
         ↓
    [Cache & Return to Client]
         ├─ Redis cache (30 min TTL)
         └─ Send with rankings & reasons
         
RESULT: Personalized feed, 50 articles, <500ms
```

### 3. RAG-Powered Synthesis

```
User Query (POST /api/synthesize/briefing)
    "What's the impact of AI regulation on tech stocks?"
         ↓
    [Embed Query]
         ├─ Convert to 1536-dim vector
         └─ Query hash for cache check
         ↓
    [Semantic Search]
         ├─ Query Pinecone: top 20 similar articles
         ├─ Rerank with BM25 if hybrid
         └─ Get top 5 most relevant
         ↓
    [Build RAG Context]
         ├─ Retrieve article content
         ├─ Extract key facts
         ├─ Identify citations
         └─ Check consistency
         ↓
    [Generate Prompt with Context]
         ├─ System prompt (role + constraints)
         ├─ User question
         ├─ Retrieved context
         └─ Citation instructions
         ↓
    [Check Response Cache]
         ├─ Hash prompt
         └─ Return cached if exists (save LLM cost!)
         ↓
    [Call Claude API]
         ├─ Stream response for real-time display
         ├─ Track token usage
         └─ Cost monitoring
         ↓
    [Verify Facts]
         ├─ Check response against sources
         ├─ Detect hallucinations
         └─ Add confidence scores
         ↓
    [Generate Follow-up Questions]
         ├─ Identify missing angles
         └─ Suggest deeper exploration
         ↓
    [Package Response]
         ├─ Main synthesis text
         ├─ Source citations + links
         ├─ Follow-up questions
         ├─ Confidence score
         └─ Generation time
         ↓
    [Cache for future queries]
         ├─ Redis: 30-min TTL
         └─ Save cost for similar future queries

RESULT: Accurate synthesis, <1.5s latency, source attribution
```

### 4. Trend Detection & Prediction

```
Article Published
         ↓
    [Extract Entities]
         ├─ Companies, people, sectors, products
         └─ Entity Linking to knowledge graph
         ↓
    [Update Entity Metrics]
         ├─ Increment mention count
         ├─ Record timestamp
         └─ Store sentiment
         ↓
    [Calculate Trends]
         ├─ Mention velocity (mentions/hour)
         ├─ Acceleration (2nd derivative)
         ├─ Sentiment momentum
         └─ Engagement trend
         ↓
    [Detect Emerging Trends]
         ├─ IF velocity > threshold AND acceleration > 0
         ├─ Mark as "emerging"
         └─ Trigger notifications
         ↓
    [Run Prediction Models]
         │
         ├─ PATTERN MATCHING
         │  ├─ Historical similarity matching
         │  ├─ Similar past events
         │  └─ Predict outcomes
         │
         ├─ TIME SERIES FORECASTING
         │  ├─ ARIMA/Prophet models
         │  ├─ Velocity forecasting
         │  └─ Predict end date
         │
         └─ SCENARIO ANALYSIS
            ├─ Entity relationships
            ├─ Sector impacts
            └─ Market implications
         ↓
    [Generate Predictions]
         ├─ Emerging story in 48h
         ├─ Sector momentum shift
         ├─ Event impact scenarios
         └─ Confidence scores
         ↓
    [Store in DB & Cache]
         ├─ Predictions table
         ├─ Track verification
         └─ Learn from results
         ↓
    [Expose in APIs]
         ├─ /api/trending/now
         ├─ /api/predictions/emerging-stories
         └─ /api/predictions/sector-momentum

RESULT: Real-time trending, 48-72h predictions, >70% accuracy
```

---

## 🔄 API Flow Examples

### Example 1: User Signup & Profile Creation

```
User Input: Email, Name, Profile Type, Interests

POST /api/auth/signup
├─ Validate email
├─ Create UserProfile
├─ Create UserSession + token
└─ Return user data & token

Client Stores token in localStorage

POST /api/profiles/update-interests
├─ Update user interests
├─ Trigger recommendation recompute
└─ Return updated profile

GET /api/feed/personalized
├─ Generate personalized feed
├─ Cache for 30 minutes
└─ Return 50 articles with rankings
```

### Example 2: Searching & Synthesis

```
User Input: "What are the latest AI regulations?"

POST /api/search/semantic
├─ Embed query
├─ Search Pinecone: top 20 similar articles
├─ Rerank & filter duplicates
└─ Return 10 most relevant with scores

User clicks "Get Synthesis"

POST /api/synthesize/briefing
├─ Check cache (same query recent?)
├─ Retrieve top 5 articles for context
├─ Build RAG prompt
├─ Check LLM response cache
├─ Call Claude API (streaming)
├─ Verify facts
└─ Return synthesis + citations + follow-ups

User: "What about impact on Tesla?"

POST /api/chat/ask
├─ Load conversation history
├─ Understand "Tesla" from context
├─ Perform semantic search with updated context
├─ Generate response considering previous discussion
└─ Save to conversation history
```

### Example 3: Real-Time Trends

```
New Articles Published About Tesla Product Launch

[NLP Processing]
├─ Extract entities: Tesla, Elon Musk, Automotive, AI
├─ Sentiment: +0.8 (positive)
├─ Topics: [AI, Automotive, Innovation]

[Trend Detection]
├─ Tesla mentions: 45 in last hour (was 10/hr)
├─ Velocity: 4.5x spike
├─ Sentiment trending positive
├─ Mark as "emerging trend"

GET /api/trending/now
├─ Return top 20 trending
├─ Tesla at rank #1
├─ Show: mention velocity, sentiment, confidence
└─ Include: "Up 450% in mentions"

GET /api/predictions/emerging-stories
├─ Model predicts: Full impact story in 24-48h
├─ Confidence: 82%
├─ Related entities: [Tesla, Elon Musk, Auto Industry]
└─ Suggested impacts: [Stock movement, Competitor response]
```

---

## 📈 Scaling Considerations

### Load Distribution

```
                    [Load Balancer]
                           |
        |__________|__________|__________|
        |          |          |          |
    [API-1]    [API-2]    [API-3]    [API-4]
    
Each instance can handle:
- 1000 concurrent users
- 100 requests/second
- <200ms response time

For 1M concurrent users need: 1000+ instances
(Use auto-scaling: Kubernetes HPA)
```

### Data Scaling

```
Single Node Limits:
├─ PostgreSQL: 1-5M articles per instance
├─ Redis: 100GB max (expensive)
├─ Pinecone: 1.5M vectors per instance

Scaling Approach:
├─ PostgreSQL: Read replicas + sharding by date
├─ Redis: Cluster mode, consistent hashing
├─ Pinecone: Multiple indices, intelligent routing
```

### Processing Pipeline

```
Articles/Hour: 10,000
├─ NLP Processing: Need 20-30 workers
│  ├─ 500 articles/worker/hour
│  └─ Use Celery queue
├─ Embedding Generation: Need 10-15 workers
│  ├─ 1000 embeddings/hour/worker
│  └─ Batch processing
└─ Trend Detection: Real-time, single service

Recommendation Computation:
├─ Run every 6 hours
├─ Takes 10-15 minutes (for all users)
├─ Cache for 6 hours
└─ Or compute on-demand if cache miss
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────┐
│         AUTHENTICATION LAYER                │
├─────────────────────────────────────────────┤
│  ├─ JWT tokens (30-day expiry)              │
│  ├─ OAuth2 for social login (future)        │
│  ├─ Session validation                      │
│  └─ Refresh token rotation                  │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│         AUTHORIZATION LAYER                 │
├─────────────────────────────────────────────┤
│  ├─ Role-based access control (RBAC)        │
│  ├─ Scope validation                        │
│  └─ Resource ownership checks               │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│      RATE LIMITING & DDoS PROTECTION        │
├─────────────────────────────────────────────┤
│  ├─ 100 requests/minute per user            │
│  ├─ 1000 requests/minute per API key        │
│  ├─ IP-based rate limiting                  │
│  └─ Burst allowance (20% of limit)          │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│      INPUT VALIDATION & SANITIZATION        │
├─────────────────────────────────────────────┤
│  ├─ SQL injection prevention (ORM)          │
│  ├─ XSS protection (output escaping)        │
│  ├─ CSRF tokens                             │
│  └─ Schema validation (Pydantic)            │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│         ENCRYPTION IN TRANSIT               │
├─────────────────────────────────────────────┤
│  ├─ TLS 1.3 for all connections             │
│  ├─ Certificate pinning (mobile)            │
│  └─ HSTS headers                            │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│       ENCRYPTION AT REST                    │
├─────────────────────────────────────────────┤
│  ├─ Database encryption (AES-256)           │
│  ├─ Sensitive fields masked                 │
│  ├─ API key rotation                        │
│  └─ Audit logging (immutable)               │
└─────────────────────────────────────────────┘
```

---

## 📊 Monitoring & Observability

```
APPLICATION METRICS
├─ Request latency (p50, p95, p99)
├─ Error rate & types
├─ Cache hit rate
├─ LLM token usage & costs
└─ Recommendation quality (CTR, engagement)

DATABASE METRICS
├─ Query latency
├─ Connection pool usage
├─ Replication lag
└─ Index efficiency

VECTOR DB METRICS
├─ Search latency
├─ QPS (queries per second)
├─ Recall @ K
└─ Storage utilization

BUSINESS METRICS
├─ Active users
├─ Engagement time
├─ Recommendation accuracy
├─ Trend prediction accuracy
└─ User satisfaction (NPS)

INFRASTRUCTURE
├─ CPU/Memory usage
├─ Network I/O
├─ Disk space
└─ Auto-scaling triggers
```

---

## 🎯 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Homepage Load | <500ms | WIP |
| Semantic Search | <200ms | WIP |
| Hybrid Search | <300ms | WIP |
| Synthesis Generation | <1.5s | WIP |
| Chat Response | <2s | WIP |
| Feed Generation | <500ms | WIP |
| P99 Latency | <2s | WIP |
| Error Rate | <0.1% | WIP |
| Availability | 99.9% | Setup phase |

---

This architecture supports scaling from thousands to millions of users while maintaining sub-2 second latencies across all operations. The modular design allows for independent scaling of each component based on bottlenecks.
