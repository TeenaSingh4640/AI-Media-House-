'use client';

import React, { useEffect, useState } from 'react';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'next/navigation';

export default function Profile() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [interests, setInterests] = useState({
    sectors: [] as string[],
    companies: [] as string[],
    topics: [] as string[]
  });
  const [newSector, setNewSector] = useState('');
  const [newCompany, setNewCompany] = useState('');
  const [newTopic, setNewTopic] = useState('');

  const profileIcons: Record<string, string> = {
    investor: '💰',
    founder: '🚀',
    student: '📚',
    general: '👤'
  };

  const addItem = (category: 'sectors' | 'companies' | 'topics', value: string) => {
    if (value.trim()) {
      setInterests({
        ...interests,
        [category]: [...interests[category], value.trim()]
      });
      if (category === 'sectors') setNewSector('');
      if (category === 'companies') setNewCompany('');
      if (category === 'topics') setNewTopic('');
    }
  };

  const removeItem = (category: 'sectors' | 'companies' | 'topics', index: number) => {
    setInterests({
      ...interests,
      [category]: interests[category].filter((_, i) => i !== index)
    });
  };

  if (!user) return null;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Profile & Preferences</h1>
          <p className="text-gray-600 text-lg\">Personalize your news experience</p>
        </div>
        <button
          onClick={() => {
            logout();
            router.push('/');
          }}
          className="px-6 py-3 text-red-600 hover:bg-red-50 rounded-xl transition font-bold border border-red-200 hover:border-red-300"
        >
          Sign Out
        </button>
      </div>

      {/* Profile Card */}
      <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl shadow-2xl p-8 text-white relative overflow-hidden border border-purple-400">
        <div className="absolute -top-20 -right-20 w-40 h-40 bg-white/10 rounded-full blur-3xl"></div>
        <div className="relative z-10 flex items-start justify-between">
          <div>
            <div className="text-7xl mb-4">{profileIcons[user.profile_type as keyof typeof profileIcons] || '👤'}</div>
            <h2 className="text-4xl font-bold mb-2">{user.name}</h2>
            <p className="text-blue-100 text-lg">{user.email}</p>
            <div className="mt-5 inline-block px-5 py-2 bg-white/20 backdrop-blur-sm rounded-xl border border-white/30">
              <p className="text-sm font-bold uppercase tracking-wide">Profile: <span className="capitalize">{user.profile_type}</span></p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-6xl animate-bounce">⭐</div>
            <p className="text-blue-100 text-sm mt-2 font-semibold">Premium Member</p>
          </div>
        </div>
      </div>

      {/* Interests Section */}
      <div className="grid grid-cols-3 gap-6">
        {/* Sectors */}
        <div className="bg-white rounded-2xl shadow-sm hover:shadow-xl transition p-8 border border-gray-100 hover:border-blue-200">
          <h3 className="text-xl font-bold text-gray-900 mb-5 flex items-center gap-2">
            <span className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">🏭</span> Sectors
          </h3>
          <div className="flex gap-2 mb-5">
            <input
              type="text"
              value={newSector}
              onChange={(e) => setNewSector(e.target.value)}
              placeholder="IT, Finance, Healthcare..."
              className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm hover:border-blue-300 transition"
              onKeyPress={(e) => e.key === 'Enter' && addItem('sectors', newSector)}
            />
            <button
              onClick={() => addItem('sectors', newSector)}
              className="px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg hover:shadow-lg transition font-bold text-sm"
            >
              +
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {interests.sectors.map((sector, idx) => (
              <div key={idx} className="bg-gradient-to-r from-blue-50 to-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-2 border border-blue-200 hover:border-blue-300 transition">
                {sector}
                <button
                  onClick={() => removeItem('sectors', idx)}
                  className="hover:text-red-600 font-bold ml-1"
                >
                  ✕
                </button>
              </div>
            ))}
            {interests.sectors.length === 0 && (
              <p className="text-gray-400 text-sm italic">Add your sectors...</p>
            )}
          </div>
        </div>

        {/* Companies */}
        <div className="bg-white rounded-2xl shadow-sm hover:shadow-xl transition p-8 border border-gray-100 hover:border-purple-200">
          <h3 className="text-xl font-bold text-gray-900 mb-5 flex items-center gap-2">
            <span className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">🏢</span> Companies
          </h3>
          <div className="flex gap-2 mb-5">
            <input
              type="text"
              value={newCompany}
              onChange={(e) => setNewCompany(e.target.value)}
              placeholder="TCS, Infosys, Google..."
              className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-sm hover:border-purple-300 transition"
              onKeyPress={(e) => e.key === 'Enter' && addItem('companies', newCompany)}
            />
            <button
              onClick={() => addItem('companies', newCompany)}
              className="px-4 py-2 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-lg hover:shadow-lg transition font-bold text-sm"
            >
              +
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {interests.companies.map((company, idx) => (
              <div key={idx} className="bg-gradient-to-r from-purple-50 to-purple-100 text-purple-700 px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-2 border border-purple-200 hover:border-purple-300 transition">
                {company}
                <button
                  onClick={() => removeItem('companies', idx)}
                  className="hover:text-red-600 font-bold ml-1"
                >
                  ✕
                </button>
              </div>
            ))}
            {interests.companies.length === 0 && (
              <p className="text-gray-400 text-sm italic">Add companies...</p>
            )}
          </div>
        </div>

        {/* Topics */}
        <div className="bg-white rounded-2xl shadow-sm hover:shadow-xl transition p-8 border border-gray-100 hover:border-pink-200">
          <h3 className="text-xl font-bold text-gray-900 mb-5 flex items-center gap-2">
            <span className="w-8 h-8 bg-pink-100 rounded-lg flex items-center justify-center">📌</span> Topics
          </h3>
          <div className="flex gap-2 mb-5">
            <input
              type="text"
              value={newTopic}
              onChange={(e) => setNewTopic(e.target.value)}
              placeholder="AI, Crypto, ESG..."
              className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 text-sm hover:border-pink-300 transition"
              onKeyPress={(e) => e.key === 'Enter' && addItem('topics', newTopic)}
            />
            <button
              onClick={() => addItem('topics', newTopic)}
              className="px-4 py-2 bg-gradient-to-r from-pink-600 to-pink-700 text-white rounded-lg hover:shadow-lg transition font-bold text-sm"
            >
              +
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {interests.topics.map((topic, idx) => (
              <div key={idx} className="bg-gradient-to-r from-pink-50 to-pink-100 text-pink-700 px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-2 border border-pink-200 hover:border-pink-300 transition">
                {topic}
                <button
                  onClick={() => removeItem('topics', idx)}
                  className="hover:text-red-600 font-bold ml-1"
                >
                  ✕
                </button>
              </div>
            ))}
            {interests.topics.length === 0 && (
              <p className="text-gray-400 text-sm italic">Add topics...</p>
            )}
          </div>
        </div>
      </div>

      {/* Preferences */}
      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl shadow-sm hover:shadow-xl transition p-8 border border-gray-100">
          <h4 className="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
            <span className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">⚙️</span> Preferences
          </h4>
          <div className="space-y-5">
            <div>
              <label className="block text-sm font-bold text-gray-900 mb-2">Content Depth</label>
              <select className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 hover:border-blue-300 transition font-medium bg-white">
                <option>Quick Summary</option>
                <option selected>Detailed Analysis</option>
                <option>Research Level</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-900 mb-2">Update Frequency</label>
              <select className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 hover:border-blue-300 transition font-medium bg-white">
                <option>Real-time</option>
                <option selected>Daily Digest</option>
                <option>Weekly Digest</option>
              </select>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-sm hover:shadow-xl transition p-8 border border-gray-100">
          <h4 className="text-lg font-bold text-gray-900 mb-5 flex items-center gap-2">
            <span className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">🌐</span> Language
          </h4>
          <div className="space-y-3">
            <button className="w-full text-left px-4 py-3 border-2 border-blue-600 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl font-bold text-blue-700 hover:shadow-md transition">
              ✓ English
            </button>
            <button className="w-full text-left px-4 py-3 border border-gray-300 rounded-xl hover:border-purple-300 hover:bg-purple-50 transition font-medium text-gray-700">
              हिंदी (Hindi)
            </button>
            <button className="w-full text-left px-4 py-3 border border-gray-300 rounded-xl hover:border-pink-300 hover:bg-pink-50 transition font-medium text-gray-700">
              தமிழ் (Tamil)
            </button>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <button className="w-full py-4 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white rounded-xl font-bold text-lg hover:shadow-2xl transition transform hover:scale-105 border border-purple-400 shadow-lg">
        💾 Save Changes
      </button>
    </div>
  );
}
