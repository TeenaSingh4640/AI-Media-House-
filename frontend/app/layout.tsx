import React from 'react';
import Link from 'next/link';
import './globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <title>My ET - AI News Platform</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="bg-gray-900">
        <div className="flex h-screen bg-gray-900">
          {/* Sidebar */}
          <aside className="w-72 bg-gray-950 border-r border-gray-800 overflow-y-auto flex flex-col">
            {/* Logo */}
            <div className="p-6 border-b border-gray-800">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-lg">M</div>
                <div>
                  <div className="text-xl font-bold text-white">My ET</div>
                  <p className="text-xs text-gray-500 font-medium">GLOBAL NEWS</p>
                </div>
              </div>
            </div>

            {/* Main Navigation */}
            <nav className="flex-1 px-3 py-6 space-y-1">
              <div className="px-3 py-2 text-xs font-bold text-gray-400 uppercase tracking-wider">Navigation</div>
              <Link href="/" className="flex items-center px-4 py-3 rounded-lg text-gray-300 hover:bg-blue-600/10 hover:text-blue-400 transition group">
                <span className="text-lg mr-3">🏠</span>
                <span className="font-medium">Home</span>
                <span className="ml-auto text-xs bg-blue-600/20 text-blue-400 px-2 py-1 rounded group-hover:bg-blue-600/30">NEW</span>
              </Link>
              <Link href="/feed" className="flex items-center px-4 py-3 rounded-lg text-gray-300 hover:bg-purple-600/10 hover:text-purple-400 transition">
                <span className="text-lg mr-3">📰</span>
                <span className="font-medium">News Feed</span>
              </Link>
              <Link href="/navigator" className="flex items-center px-4 py-3 rounded-lg text-gray-300 hover:bg-pink-600/10 hover:text-pink-400 transition">
                <span className="text-lg mr-3">🤖</span>
                <span className="font-medium">AI Navigator</span>
              </Link>

              <div className="px-3 py-2 text-xs font-bold text-gray-400 uppercase tracking-wider mt-6">Discover</div>
              <button className="w-full flex items-center px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 transition">
                <span className="text-lg mr-3">📈</span>
                <span className="font-medium">Markets</span>
              </button>
              <button className="w-full flex items-center px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 transition">
                <span className="text-lg mr-3">⭐</span>
                <span className="font-medium">Watchlist</span>
              </button>
              <button className="w-full flex items-center px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 transition">
                <span className="text-lg mr-3">💼</span>
                <span className="font-medium">Companies</span>
              </button>

              <div className="px-3 py-2 text-xs font-bold text-gray-400 uppercase tracking-wider mt-6">Account</div>
              <Link href="/profile" className="flex items-center px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 transition">
                <span className="text-lg mr-3">⚙️</span>
                <span className="font-medium">Settings</span>
              </Link>
            </nav>

            {/* Bottom Card */}
            <div className="p-4 border-t border-gray-800">
              <div className="bg-gradient-to-br from-blue-600/10 to-purple-600/10 p-4 rounded-lg border border-blue-600/20 backdrop-blur-sm">
                <h4 className="font-bold text-sm text-white mb-1">🚀 Pro Features</h4>
                <p className="text-xs text-gray-400 leading-relaxed mb-3">AI synthesis, custom alerts, and more</p>
                <button className="w-full py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-xs font-bold rounded-lg hover:shadow-lg transition">Upgrade Now</button>
              </div>
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1 overflow-y-auto bg-gray-900">
            {/* Top Bar */}
            <div className="sticky top-0 bg-gray-950/80 backdrop-blur-xl border-b border-gray-800 px-8 py-4 flex items-center justify-between z-20 shadow-lg">
              <div className="flex items-center gap-4">
                <div className="p-2 hover:bg-gray-800 rounded-lg transition cursor-pointer">📍</div>
                <div>
                  <h1 className="text-xl font-bold text-white">News Platform</h1>
                  <p className="text-xs text-gray-500">Real-time market intelligence</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="hidden md:flex items-center bg-gray-800 rounded-lg px-4 py-2 focus-within:ring-2 focus-within:ring-blue-500">
                  <span className="text-gray-500">🔍</span>
                  <input
                    type="text"
                    placeholder="Search news, stocks, topics..."
                    className="ml-2 bg-transparent text-white placeholder-gray-500 outline-none w-64"
                  />
                </div>
                <button className="p-2 hover:bg-gray-800 rounded-lg transition text-gray-400 hover:text-white">📊</button>
                <button className="p-2 hover:bg-gray-800 rounded-lg transition text-gray-400 hover:text-white">🔔</button>
                <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">U</div>
              </div>
            </div>

            <div className="p-8">
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}
