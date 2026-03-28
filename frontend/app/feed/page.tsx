'use client';

import React, { useEffect, useState } from 'react';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'next/navigation';

interface Article {
  id: number;
  title: string;
  url: string;
  summary: string;
  sentiment: number;
  tags: string[];
  published_at: string;
}

export default function Feed() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    if (!user) {
      router.push('/');
      return;
    }

    fetchFeed();
  }, [user, router]);

  const fetchFeed = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/feed/personalized?user_id=${user?.id}`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );
      const data = await response.json();
      setArticles(data.articles || []);
    } catch (error) {
      console.error('Failed to fetch feed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  // Mock data for featured articles and recommendations
  const featuredArticle = articles[0] || {
    id: 1,
    title: "Inside Microsoft's New Quantum Computer Breakthrough",
    summary: "Microsoft announces major breakthrough in quantum computing with practical applications emerging next year.",
    sentiment: 0.8,
    tags: ["Technology", "Innovation"],
    url: "#",
    published_at: new Date().toISOString()
  };

  const recommendations = [
    { id: 1, title: "Nasdaq surges 2.5% on AI optimism", category: "Market" },
    { id: 2, title: "New regulation impacts crypto exchanges", category: "Policy" },
    { id: 3, title: "Indian startups raise record $500M", category: "Startups" }
  ];

  const analytics = [
    { label: "Read Time", value: "42 min", change: "+12%" },
    { label: "Articles", value: "156", change: "+8%" },
    { label: "Topics", value: "23", change: "+5%" }
  ];

  const marketData = [
    { name: "Sensex", value: "74,532", change: "+1.23%", status: "up" },
    { name: "Nifty 50", value: "22,641", change: "+0.98%", status: "up" },
    { name: "BTC", value: "$42,123", change: "-2.45%", status: "down" }
  ];

  return (
    <div className="space-y-8">
      {/* Dashboard Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Your Feed</h1>
          <p className="text-gray-400">Personalized for <span className="font-semibold text-blue-400 capitalize">{user.profile_type}</span> • Last updated: 2 min ago</p>
        </div>
        <button
          onClick={() => {
            logout();
            router.push('/');
          }}
          className="px-4 py-2 bg-red-600/10 text-red-400 rounded-lg hover:bg-red-600/20 transition text-sm font-medium"
        >
          Sign Out
        </button>
      </div>

      {/* Market Data Ticker */}
      <div className="grid grid-cols-3 gap-4">
        {marketData.map((market, idx) => (
          <div key={idx} className="bg-gray-950 border border-gray-800 rounded-lg p-4 hover:border-blue-700/50 transition">
            <p className="text-xs text-gray-500 font-medium mb-2">{market.name}</p>
            <div className="flex items-end justify-between">
              <div>
                <p className="text-2xl font-bold text-white">{market.value}</p>
                <p className={`text-xs font-semibold mt-1 ${market.status === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                  {market.change}
                </p>
              </div>
              <div className="text-2xl">{market.status === 'up' ? '📈' : '📉'}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Featured Article */}
      {articles.length > 0 && (
        <div className="bg-gradient-to-br from-blue-600/20 to-purple-600/20 border border-blue-600/30 rounded-2xl shadow-2xl p-8 text-white overflow-hidden relative backdrop-blur-sm">
          <div className="absolute -top-20 -right-20 w-40 h-40 bg-blue-600/20 rounded-full blur-3xl"></div>
          <div className="absolute -bottom-20 -left-20 w-40 h-40 bg-purple-600/20 rounded-full blur-3xl"></div>
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-4">
              <span className="px-4 py-1 bg-blue-600/30 backdrop-blur-sm rounded-full text-xs font-bold uppercase tracking-wider border border-blue-500/50">⭐ Trending</span>
              <span className="text-xs text-blue-300 font-semibold">Top Story</span>
            </div>
            <h2 className="text-4xl font-bold mb-4 leading-tight">{featuredArticle.title}</h2>
            <p className="text-blue-100 mb-6 text-lg leading-relaxed">{featuredArticle.summary}</p>
            <div className="flex items-center justify-between">
              <div className="flex gap-2 flex-wrap">
                {featuredArticle.tags.map((tag) => (
                  <span key={tag} className="px-4 py-1 bg-white/10 backdrop-blur-sm rounded-lg text-xs font-semibold border border-white/20">
                    {tag}
                  </span>
                ))}
              </div>
              <button className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold transition duration-200 whitespace-nowrap">
                Read Full Story →
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content Grid */}
      <div className="grid grid-cols-3 gap-6">
        {/* Articles Section (2 cols) */}
        <div className="col-span-2 space-y-4">
          {/* Filter Tabs */}
          <div className="flex gap-3">
            {['All', 'Markets', 'Tech', 'Startups', 'Policy'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab.toLowerCase())}
                className={`px-4 py-2 rounded-lg font-medium text-sm transition ${
                  activeTab === tab.toLowerCase()
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Articles List */}
          {loading ? (
            <div className="text-center py-16">
              <div className="inline-block animate-pulse text-5xl mb-4">⏳</div>
              <p className="text-gray-400 font-medium">Loading articles...</p>
            </div>
          ) : articles.length === 0 ? (
            <div className="bg-gray-950 border border-gray-800 rounded-2xl p-16 text-center">
              <p className="text-gray-400 font-medium text-lg">📰 No articles yet. Customize your interests to get started!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {articles.slice(0, 5).map((article, idx) => (
                <div key={article.id} className="bg-gray-950 border border-gray-800 rounded-xl p-6 hover:border-blue-600/50 transition group">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-xs bg-blue-600/30 text-blue-300 px-2.5 py-1 rounded-full font-bold">#{idx + 1}</span>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                          article.sentiment > 0 ? 'bg-green-600/30 text-green-300' :
                          article.sentiment < 0 ? 'bg-red-600/30 text-red-300' :
                          'bg-gray-600/30 text-gray-300'
                        }`}>
                          {article.sentiment > 0 ? '↗ Positive' : article.sentiment < 0 ? '↘ Negative' : '→ Neutral'}
                        </span>
                      </div>
                      <h3 className="text-lg font-bold text-white group-hover:text-blue-400 transition">{article.title}</h3>
                    </div>
                  </div>
                  
                  <p className="text-gray-400 text-sm mb-4 line-clamp-2">{article.summary}</p>
                  
                  <div className="flex gap-2 mb-4 flex-wrap">
                    {article.tags.slice(0, 3).map((tag) => (
                      <span key={tag} className="bg-blue-600/20 text-blue-300 text-xs px-2.5 py-1 rounded-full border border-blue-600/30 font-semibold">
                        {tag}
                      </span>
                    ))}
                  </div>
                  
                  <div className="flex justify-between items-center pt-3 border-t border-gray-800">
                    <span className="text-xs text-gray-500">
                      {new Date(article.published_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </span>
                    <a
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-400 hover:text-blue-300 font-bold text-sm transition inline-flex items-center gap-1"
                    >
                      Read →
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Sidebar (1 col) */}
        <div className="space-y-4">
          {/* Stats */}
          <div className="bg-gray-950 border border-gray-800 rounded-xl p-5">
            <h4 className="text-sm font-bold text-white mb-4 uppercase tracking-wide">📊 Your Stats</h4>
            {analytics.map((stat, idx) => (
              <div key={idx} className="mb-4 last:mb-0">
                <div className="flex justify-between items-center mb-1">
                  <p className="text-xs text-gray-400">{stat.label}</p>
                  <p className="text-xs text-green-400 font-bold">{stat.change}</p>
                </div>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
              </div>
            ))}
          </div>

          {/* Trending */}
          <div className="bg-gray-950 border border-gray-800 rounded-xl p-5">
            <h4 className="text-sm font-bold text-white mb-4 uppercase tracking-wide">🔥 Trending Now</h4>
            <div className="space-y-2">
              {recommendations.map((rec) => (
                <div key={rec.id} className="p-3 bg-gray-900/50 border border-gray-800/50 rounded-lg hover:border-blue-600/50 cursor-pointer transition">
                  <p className="text-sm font-semibold text-gray-200 line-clamp-1">{rec.title}</p>
                  <p className="text-xs text-blue-400 font-bold mt-1">{rec.category}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Upgrade Card */}
          <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-purple-600/30 rounded-xl p-5 backdrop-blur-sm">
            <h4 className="text-sm font-bold text-white mb-2">✨ Unlock More</h4>
            <p className="text-xs text-gray-300 mb-4 leading-relaxed">Get custom alerts, advanced search, and AI synthesis</p>
            <button className="w-full py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-xs font-bold rounded-lg hover:shadow-lg transition">
              Upgrade Pro
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
