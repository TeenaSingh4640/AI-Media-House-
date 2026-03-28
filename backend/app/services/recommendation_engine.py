"""
Recommendation Engine & Personalization Service
Hybrid recommendation system combining collaborative filtering, content-based, and trending signals
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np


class RecommendationEngine:
    """
    Hybrid recommendation system for personalized feed generation
    """
    
    def __init__(self):
        self.collaborative_filter = CollaborativeFiltering()
        self.content_based_filter = ContentBasedFilter()
        self.trending_ranker = TrendingRanker()
        self.diversity_optimizer = DiversityOptimizer()
    
    async def generate_personalized_feed(
        self,
        user_id: int,
        limit: int = 50,
        include_trending: bool = True,
        include_saved_related: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized feed combining multiple signals
        
        Returns: [
            {
                "article_id": 123,
                "title": "Tesla Q4 Earnings Beat",
                "rank": 1,
                "relevance_score": 0.92,
                "recommendation_reason": "You follow Tesla and this matches your investment thesis",
                "personalization_sources": ["content_based", "trending", "collaborative"]
            }
        ]
        """
        # 1. Get user profile and interests
        user_profile = await self._get_user_profile(user_id)
        
        # 2. Generate recommendations from each source
        collaborative_recs = await self.collaborative_filter.recommend(user_id, limit)
        content_recs = await self.content_based_filter.recommend(user_id, user_profile, limit)
        trending_recs = await self.trending_ranker.get_trending(user_profile, limit) if include_trending else []
        
        # 3. Merge and weight recommendations
        merged_recs = await self._merge_recommendations(
            collaborative_recs, content_recs, trending_recs, user_profile
        )
        
        # 4. Optimize for diversity (avoid repetition)
        diverse_recs = await self.diversity_optimizer.optimize(merged_recs, limit)
        
        # 5. Rank by relevance
        ranked_recs = sorted(diverse_recs, key=lambda x: x['relevance_score'], reverse=True)[:limit]
        
        # 6. Add explanations for transparency
        explained_recs = await self._add_explanations(ranked_recs, user_profile)
        
        return explained_recs
    
    async def _get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Get user interests, history, and preferences"""
        # TODO: Query user_profiles table
        return {}
    
    async def _merge_recommendations(
        self,
        collaborative: List[Dict],
        content_based: List[Dict],
        trending: List[Dict],
        user_profile: Dict
    ) -> List[Dict]:
        """
        Merge recommendations from different sources with weighted scoring
        
        Weights:
        - Collaborative: 40% (what similar users liked)
        - Content-based: 35% (articles matching user interests)
        - Trending: 25% (current trending topics)
        """
        scores = {}
        
        # Collaborative filtering (40%)
        for rec in collaborative:
            article_id = rec['article_id']
            scores[article_id] = scores.get(article_id, 0) + rec['score'] * 0.40
        
        # Content-based (35%)
        for rec in content_based:
            article_id = rec['article_id']
            scores[article_id] = scores.get(article_id, 0) + rec['score'] * 0.35
        
        # Trending (25%)
        for rec in trending:
            article_id = rec['article_id']
            scores[article_id] = scores.get(article_id, 0) + rec['score'] * 0.25
        
        # Normalize scores
        merged = [
            {'article_id': aid, 'relevance_score': score / 100}
            for aid, score in scores.items()
        ]
        
        return merged
    
    async def _add_explanations(self, recs: List[Dict], user_profile: Dict) -> List[Dict]:
        """Add human-readable explanations for each recommendation"""
        for rec in recs:
            rec['personalization_reason'] = await self._generate_reason(rec, user_profile)
        return recs
    
    async def _generate_reason(self, rec: Dict, user_profile: Dict) -> str:
        """Generate explanation for why article was recommended"""
        # Examples:
        # "Matches your interest in AI and recommender systems"
        # "Trending among tech investors who follow your interests"
        # "Related to Tesla, which you've been following"
        return ""


class CollaborativeFiltering:
    """
    Collaborative filtering: recommend articles liked by similar users
    """
    
    async def recommend(self, user_id: int, limit: int = 50) -> List[Dict]:
        """
        Find similar users and recommend articles they engaged with
        
        Algorithm:
        1. Build user-item engagement matrix
        2. Calculate user similarity using cosine similiarity
        3. Find top-K similar users
        4. Get articles from similar users not yet seen by current user
        5. Score by weighted ratings
        """
        
        # 1. Get user's engagement history
        user_engagement = await self._get_user_engagement(user_id)
        
        # 2. Find similar users
        similar_users = await self._find_similar_users(user_id, user_engagement, top_k=20)
        
        # 3. Get articles from similar users
        candidate_articles = await self._get_articles_from_similar_users(similar_users, user_id)
        
        # 4. Score by weighted engagement
        scored_articles = await self._score_by_similar_user_ratings(candidate_articles, similar_users)
        
        return scored_articles[:limit]
    
    async def _get_user_engagement(self, user_id: int) -> Dict[int, float]:
        """Get articles user has engaged with and engagement scores"""
        # Returns: {article_id: engagement_score}
        return {}
    
    async def _find_similar_users(self, user_id: int, engagement: Dict, top_k: int = 20) -> List[int]:
        """Find top-K users most similar to current user"""
        # Uses cosine similarity on engagement vectors
        return []
    
    async def _get_articles_from_similar_users(self, similar_users: List[int], user_id: int) -> List[Dict]:
        """Get articles engaged by similar users but not by current user"""
        return []
    
    async def _score_by_similar_user_ratings(self, articles: List[Dict], similar_users: List[int]) -> List[Dict]:
        """Score articles by ratings from similar users"""
        return articles


class ContentBasedFilter:
    """
    Content-based filtering: recommend articles similar to user's interests
    """
    
    async def recommend(self, user_id: int, user_profile: Dict, limit: int = 50) -> List[Dict]:
        """
        Recommend articles matching user interests
        
        Algorithm:
        1. Extract user interests (sectors, companies, topics)
        2. Get recent articles in those topics
        3. Match user expertise level (beginner/intermediate/advanced)
        4. Score by relevance to interests
        """
        
        # 1. Extract interests
        interests = await self._extract_user_interests(user_profile)
        
        # 2. Get candidate articles
        candidates = await self._get_articles_matching_interests(interests)
        
        # 3. Filter by expertise level
        expertise_filtered = await self._filter_by_expertise(candidates, user_profile['expertise_level'])
        
        # 4. Score by relevance
        scored = await self._score_by_interest_relevance(expertise_filtered, interests)
        
        return scored[:limit]
    
    async def _extract_user_interests(self, user_profile: Dict) -> Dict[str, List[str]]:
        """Extract user interests from profile"""
        return {
            'sectors': user_profile.get('interests', {}).get('sectors', []),
            'companies': user_profile.get('interests', {}).get('companies', []),
            'topics': user_profile.get('interests', {}).get('topics', []),
            'regions': user_profile.get('interests', {}).get('regions', [])
        }
    
    async def _get_articles_matching_interests(self, interests: Dict[str, List[str]]) -> List[Dict]:
        """Get articles matching any of user's interests"""
        # Query articles with matching entities/topics
        return []
    
    async def _filter_by_expertise(self, articles: List[Dict], expertise_level: str) -> List[Dict]:
        """
        Filter articles by user expertise level
        Beginner: simpler summaries, overview articles
        Intermediate: analysis pieces
        Advanced: deep technical analysis, research papers
        """
        return articles
    
    async def _score_by_interest_relevance(self, articles: List[Dict], interests: Dict) -> List[Dict]:
        """Score articles by how well they match user interests"""
        return articles


class TrendingRanker:
    """
    Rank trending articles and topics for feed
    """
    
    async def get_trending(self, user_profile: Dict, limit: int = 20) -> List[Dict]:
        """
        Get trending articles relevant to user profile
        Combines global trends with user interests
        """
        
        # 1. Get trending articles
        trending_articles = await self._get_trending_articles(limit * 2)
        
        # 2. Filter by relevance to user interests
        relevant_trending = await self._filter_by_interest_relevance(
            trending_articles, user_profile
        )
        
        # 3. Calculate trend scores
        scored = await self._calculate_trend_scores(relevant_trending)
        
        return scored[:limit]
    
    async def _get_trending_articles(self, limit: int) -> List[Dict]:
        """Get articles from Trend table"""
        # TODO: Query trends table and get associated articles
        return []
    
    async def _filter_by_interest_relevance(self, articles: List[Dict], user_profile: Dict) -> List[Dict]:
        """Filter trending articles relevant to user"""
        interests = user_profile.get('interests', {})
        filtered = []
        
        for article in articles:
            if self._has_interest_overlap(article, interests):
                filtered.append(article)
        
        return filtered
    
    def _has_interest_overlap(self, article: Dict, interests: Dict) -> bool:
        """Check if article has any overlap with user interests"""
        article_entities = article.get('entities', {})
        
        # Check companies
        for company in interests.get('companies', []):
            if company in article_entities.get('companies', []):
                return True
        
        # Check sectors
        for sector in interests.get('sectors', []):
            if sector in article_entities.get('sectors', []):
                return True
        
        # Check topics
        for topic in interests.get('topics', []):
            if topic in article.get('topics', []):
                return True
        
        return False
    
    async def _calculate_trend_scores(self, articles: List[Dict]) -> List[Dict]:
        """Score articles by trend strength"""
        return articles


class DiversityOptimizer:
    """
    Ensure diversity in recommendations (avoid editorial bias)
    """
    
    async def optimize(self, recommendations: List[Dict], limit: int) -> List[Dict]:
        """
        Optimize for diversity:
        - Different sectors
        - Different article types (analysis, news, opinion)
        - Different time horizons
        - Different sources
        """
        
        if len(recommendations) <= limit:
            return recommendations
        
        # Simple greedy diversity algorithm
        diverse = []
        sector_coverage = set()
        type_coverage = set()
        
        for rec in sorted(recommendations, key=lambda x: x['relevance_score'], reverse=True):
            article = rec['article']
            
            # Check if adding this adds diversity
            sectors = article.get('entities', {}).get('sectors', [])
            article_type = article.get('article_type', 'news')
            
            # Prefer articles that add new sectors/types
            if sectors[0] not in sector_coverage or article_type not in type_coverage:
                diverse.append(rec)
                if sectors:
                    sector_coverage.add(sectors[0])
                type_coverage.add(article_type)
            elif len(diverse) < limit * 0.7:  # Allow some repetition
                diverse.append(rec)
            
            if len(diverse) >= limit:
                break
        
        return diverse


print("[OK] Advanced Recommendation Engine loaded")
