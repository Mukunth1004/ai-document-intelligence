'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';

export default function DashboardPage() {
  const router = useRouter();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/auth/login');
      return;
    }

    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await apiClient.listDocuments();
      setDocuments(response.data.documents);
    } catch (error) {
      console.error('Failed to load documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    apiClient.clearToken();
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-3xl font-bold text-gray-900">Documents</h2>
            <Link
              href="/dashboard/documents"
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            >
              Upload Document
            </Link>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <p className="text-gray-600">Loading documents...</p>
            </div>
          ) : documents.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600 mb-4">No documents uploaded yet</p>
              <Link
                href="/dashboard/documents"
                className="text-indigo-600 hover:underline"
              >
                Upload your first document
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {documents.map((doc: any) => (
                <div
                  key={doc.id}
                  className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
                >
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {doc.file_name}
                  </h3>
                  <p className="text-sm text-gray-600 mb-4">
                    {(doc.file_size / 1024).toFixed(2)} KB • {doc.processing_status}
                  </p>
                  <div className="flex gap-2">
                    <Link
                      href={`/dashboard/documents/${doc.id}/chat`}
                      className="flex-1 px-3 py-2 bg-indigo-600 text-white text-sm rounded hover:bg-indigo-700 transition text-center"
                    >
                      Chat
                    </Link>
                    <button className="flex-1 px-3 py-2 bg-red-100 text-red-600 text-sm rounded hover:bg-red-200 transition">
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
