'use client';

import React from 'react';

interface Article {
  id: number;
  title: string;
  source: string;
  sentiment: number;
  tags: string[];
}

interface SourceArticlesProps {
  articles: Article[];
}

export default function SourceArticles({ articles }: SourceArticlesProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-bold mb-4">Source Articles</h3>
      <div className="space-y-3">
        {articles.map((article) => (
          <div key={article.id} className="p-3 border border-gray-200 rounded hover:bg-gray-50">
            <h4 className="font-semibold text-primary">{article.title}</h4>
            <div className="flex justify-between items-center mt-2">
              <span className="text-sm text-gray-600">{article.source}</span>
              <span className={`text-xs px-2 py-1 rounded ${
                article.sentiment > 0 ? 'bg-green-100 text-green-700' :
                article.sentiment < 0 ? 'bg-red-100 text-red-700' :
                'bg-gray-100 text-gray-700'
              }`}>
                {article.sentiment > 0 ? 'Positive' : article.sentiment < 0 ? 'Negative' : 'Neutral'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
