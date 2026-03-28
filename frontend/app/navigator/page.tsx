'use client';

import React, { useState } from 'react';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'next/navigation';

export default function Navigator() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [topic, setTopic] = useState('');
  const [synthesis, setSynthesis] = useState('');
  const [questions, setQuestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeQuestion, setActiveQuestion] = useState<number | null>(null);

  if (!user) return null;

  const handleSynthesize = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setSynthesis('');
    setQuestions([]);
    setActiveQuestion(null);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/navigator/synthesize`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            topic,
            article_ids: [1, 2, 3],
            depth: 'standard'
          })
        }
      );
      const data = await response.json();
      setSynthesis(data.synthesis);
      setQuestions(data.follow_up_questions);
    } catch (error) {
      console.error('Synthesis failed:', error);
      alert('Failed to generate synthesis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">📊 News Navigator</h1>
        <p className="text-gray-600">AI-powered synthesis of multiple articles into interactive briefings</p>
      </div>

      {/* Search Section */}
      <form onSubmit={handleSynthesize} className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-2xl shadow-2xl p-8 text-white relative overflow-hidden border border-purple-400">
        <div className="absolute -top-20 -right-20 w-40 h-40 bg-white/10 rounded-full blur-3xl"></div>
        <label className="block text-lg font-bold mb-4 relative z-10">What story would you like to explore?</label>
        <div className="flex gap-3 relative z-10">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="E.g., AI regulation, Union Budget, Startup funding trends"
            className="flex-1 px-6 py-4 border border-white/30 bg-white/10 backdrop-blur-sm rounded-xl focus:outline-none focus:ring-2 focus:ring-white text-white placeholder-white/70 transition hover:bg-white/20 font-medium"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-white text-blue-600 px-8 py-4 rounded-xl hover:bg-blue-50 disabled:opacity-50 font-bold transition transform hover:scale-105 shadow-lg disabled:hover:scale-100"
          >
            {loading ? '⏳ Synthesizing...' : '✨ Synthesize'}
          </button>
        </div>
      </form>

      {/* Results */}
      {synthesis && (
        <div className="grid grid-cols-3 gap-6 animate-fadeIn">
          {/* Main synthesis - 2 columns */}
          <div className="col-span-2 space-y-6">
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 hover:shadow-2xl transition">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold">AI</div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">Executive Briefing</h2>
                  <p className="text-xs text-gray-500 font-medium">AI-Synthesized Analysis</p>
                </div>
              </div>
              
              <div className="space-y-4 text-gray-700 leading-relaxed">
                {synthesis.split('\n').map((line, idx) => (
                  line.trim() && (
                    <p key={idx} className="text-base first:font-semibold first:text-lg first:text-gray-900">
                      {line}
                    </p>
                  )
                ))}
              </div>

              <div className="mt-8 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-200 flex items-start gap-3">
                <span className="text-xl flex-shrink-0 mt-1">💡</span>
                <p className="text-sm text-gray-700">
                  <strong className="text-gray-900">Pro Tip:</strong> Click on any follow-up question to get deeper insights.
                </p>
              </div>
            </div>
          </div>

          {/* Questions Sidebar - 1 column */}
          <div className="col-span-1">
            <div className="bg-white rounded-2xl shadow-xl p-6 sticky top-24 border border-gray-100 hover:shadow-2xl transition">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600 font-bold">?</span>
                Questions
              </h3>
              <div className="space-y-2">
                {questions.map((question, idx) => (
                  <button
                    key={idx}
                    onClick={() => setActiveQuestion(activeQuestion === idx ? null : idx)}
                    className={`w-full text-left p-4 rounded-xl border-2 transition duration-300 transform hover:scale-105 font-medium text-sm ${
                      activeQuestion === idx
                        ? 'border-purple-600 bg-gradient-to-r from-purple-50 to-pink-50 text-purple-900'
                        : 'border-gray-200 text-gray-700 hover:border-purple-300 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex gap-3">
                      <span className="flex-shrink-0 font-bold text-purple-600">#{idx + 1}</span>
                      <p className="line-clamp-2">{question}</p>
                    </div>
                  </button>
                ))}
              </div>

              <button className="w-full mt-6 px-4 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-bold hover:shadow-lg transition duration-300 transform hover:scale-105">
                📥 Export Briefing
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!synthesis && !loading && (
        <div className="space-y-8">
          <div className="text-center py-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Welcome to News Navigator</h2>
            <p className="text-gray-600 text-lg">Search for any topic to get AI-powered synthesis from multiple articles</p>
          </div>
          
          <div className="grid grid-cols-4 gap-4">
            {[
              { icon: '🔍', title: 'Smart Search', desc: 'Find any topic instantly', color: 'blue' },
              { icon: '🤖', title: 'AI Synthesis', desc: 'Powered by Claude', color: 'purple' },
              { icon: '📚', title: 'Deep Dive', desc: 'Comprehensive analysis', color: 'pink' },
              { icon: '❓', title: 'Follow-Ups', desc: 'Ask clarifying questions', color: 'orange' }
            ].map((feature, idx) => (
              <div key={idx} className="bg-white rounded-2xl shadow-sm hover:shadow-xl transition duration-300 p-6 border border-gray-100 hover:border-blue-200 group cursor-pointer transform hover:scale-105">
                <div className="text-5xl mb-3 group-hover:scale-110 transition">{feature.icon}</div>
                <h4 className="font-bold text-gray-900 mb-1 text-lg">{feature.title}</h4>
                <p className="text-sm text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
