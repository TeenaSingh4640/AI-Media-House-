'use client';

import React, { useState } from 'react';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [profileType, setProfileType] = useState('investor');
  const [isSignup, setIsSignup] = useState(false);
  const [error, setError] = useState('');
  const { signup, login, isLoading } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      if (isSignup) {
        await signup(email, name, profileType, {
          sectors: [],
          companies: [],
          topics: []
        });
      } else {
        await login(email);
      }
      router.push('/feed');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Authentication failed';
      setError(errorMessage);
      console.error('Auth error:', error);
    }
  };

  if (user) {
    router.push('/feed');
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Animated background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20"></div>
      </div>

      <div className="relative flex items-center justify-center min-h-screen px-4">
        <div className="w-full max-w-md">
          {/* Card */}
          <div className="bg-white bg-opacity-95 backdrop-blur rounded-2xl shadow-2xl p-8">
            {/* Header */}
            <div className="mb-8">
              <div className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                📰 My ET
              </div>
              <p className="text-gray-600 text-lg">AI-Powered Business News</p>
            </div>

            {/* Form Section */}
            <form onSubmit={handleSubmit} className="space-y-4">
              {isSignup && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                    <input
                      type="text"
                      placeholder="Your name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Profile Type</label>
                    <select
                      value={profileType}
                      onChange={(e) => setProfileType(e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                    >
                      <option value="investor">💰 Investor</option>
                      <option value="founder">🚀 Startup Founder</option>
                      <option value="student">📚 Student</option>
                      <option value="general">👤 General Reader</option>
                    </select>
                  </div>
                </>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                <input
                  type="email"
                  placeholder="your@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg hover:shadow-lg disabled:opacity-50 font-semibold transition transform hover:scale-105"
              >
                {isLoading ? '⏳ Loading...' : isSignup ? '✨ Create Account' : '🔓 Sign In'}
              </button>

              {error && (
                <div className="text-red-600 text-sm text-center p-2 bg-red-50 rounded-lg">
                  {error}
                </div>
              )}
            </form>

            {/* Toggle */}
            <button
              onClick={() => {
                setIsSignup(!isSignup);
                setEmail('');
                setName('');
              }}
              className="w-full mt-4 text-blue-600 hover:text-purple-600 text-sm font-medium transition"
            >
              {isSignup ? '👉 Already have an account? Sign In' : '✍️ Need an account? Sign Up'}
            </button>

            {/* Divider */}
            <div className="my-6 flex items-center">
              <div className="flex-1 h-px bg-gray-300"></div>
              <span className="px-3 text-sm text-gray-500">Features</span>
              <div className="flex-1 h-px bg-gray-300"></div>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 bg-blue-50 rounded-lg">
                <div className="text-2xl mb-1">🎯</div>
                <p className="text-xs font-semibold text-gray-800">Personalized Feed</p>
              </div>
              <div className="p-3 bg-purple-50 rounded-lg">
                <div className="text-2xl mb-1">🤖</div>
                <p className="text-xs font-semibold text-gray-800">AI Synthesis</p>
              </div>
              <div className="p-3 bg-indigo-50 rounded-lg">
                <div className="text-2xl mb-1">💬</div>
                <p className="text-xs font-semibold text-gray-800">Q&A Briefing</p>
              </div>
              <div className="p-3 bg-pink-50 rounded-lg">
                <div className="text-2xl mb-1">📈</div>
                <p className="text-xs font-semibold text-gray-800">Smart Tracking</p>
              </div>
            </div>
          </div>

          {/* Footer */}
          <p className="text-center text-gray-300 text-sm mt-6">
            The future of business news is here
          </p>
        </div>
      </div>
    </div>
  );
}
