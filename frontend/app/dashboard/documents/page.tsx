'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';

export default function DocumentsPage() {
  const router = useRouter();
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      await handleFile(files[0]);
    }
  };

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      await handleFile(files[0]);
    }
  };

  const handleFile = async (file: File) => {
    const allowedTypes = ['.pdf', '.txt', '.docx', '.md'];
    const fileExt = '.' + file.name.split('.').pop()?.toLowerCase();

    if (!allowedTypes.includes(fileExt)) {
      alert('Please upload a PDF, TXT, DOCX, or Markdown file');
      return;
    }

    setUploading(true);
    setUploadProgress(0);

    try {
      const response = await apiClient.uploadDocument(file);
      setUploadProgress(100);
      setTimeout(() => {
        router.push('/dashboard');
      }, 1000);
    } catch (error) {
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link href="/dashboard" className="text-indigo-600 hover:underline">
            ← Back to Dashboard
          </Link>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Upload Document</h1>

        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-12 text-center transition ${
            dragActive
              ? 'border-indigo-600 bg-indigo-50'
              : 'border-gray-300 bg-white'
          }`}
        >
          <div className="mb-4">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>

          <p className="text-lg font-semibold text-gray-900 mb-2">
            Drag and drop your file
          </p>
          <p className="text-gray-600 mb-4">or</p>

          <label className="inline-block">
            <input
              type="file"
              onChange={handleChange}
              disabled={uploading}
              className="hidden"
              accept=".pdf,.txt,.docx,.md"
            />
            <button
              onClick={() => {
                const input = document.querySelector('input[type="file"]') as HTMLInputElement;
                input?.click();
              }}
              disabled={uploading}
              className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
            >
              {uploading ? 'Uploading...' : 'Browse Files'}
            </button>
          </label>

          <p className="text-sm text-gray-500 mt-4">
            Supported formats: PDF, TXT, DOCX, Markdown (Max 100 MB)
          </p>

          {uploading && uploadProgress > 0 && (
            <div className="mt-6">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-indigo-600 h-2 rounded-full transition-all"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-600 mt-2">{uploadProgress}% uploaded</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
