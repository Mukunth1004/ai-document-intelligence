'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="flex flex-col items-center justify-center min-h-screen px-4">
        <div className="text-center max-w-2xl">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            AI Document Intelligence
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Intelligent Q&A system for document analysis using Retrieval-Augmented Generation (RAG)
          </p>

          <div className="space-y-4 mb-8">
            <p className="text-gray-700">
              Upload your documents and ask intelligent questions powered by Claude AI.
            </p>
            <ul className="text-left space-y-2 text-gray-700">
              <li className="flex items-center">
                <span className="mr-2">✓</span>
                Support for PDF, DOCX, TXT, and Markdown files
              </li>
              <li className="flex items-center">
                <span className="mr-2">✓</span>
                Fast semantic search with vector embeddings
              </li>
              <li className="flex items-center">
                <span className="mr-2">✓</span>
                Context-aware responses from Claude AI
              </li>
              <li className="flex items-center">
                <span className="mr-2">✓</span>
                <500ms response time with caching
              </li>
            </ul>
          </div>

          <div className="flex gap-4 justify-center">
            {isLoggedIn ? (
              <Link
                href="/dashboard"
                className="px-8 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition"
              >
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link
                  href="/auth/login"
                  className="px-8 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition"
                >
                  Login
                </Link>
                <Link
                  href="/auth/register"
                  className="px-8 py-3 bg-white text-indigo-600 border-2 border-indigo-600 rounded-lg font-semibold hover:bg-indigo-50 transition"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
