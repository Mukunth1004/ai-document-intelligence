import axios, { AxiosInstance } from 'axios';

// Determine API URL based on environment
const getApiUrl = () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  if (!apiUrl) {
    // Default for development
    return 'http://localhost:3000/_/backend';
  }

  // Handle relative URLs (for production on Vercel)
  if (apiUrl.startsWith('//')) {
    return apiUrl;
  }

  return apiUrl;
};

const API_URL = getApiUrl();

class APIClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.client.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });

    this.loadToken();
  }

  private loadToken() {
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('access_token');
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  }

  // Auth endpoints
  register(email: string, password: string, fullName: string) {
    return this.client.post('/api/v1/auth/register', {
      email,
      password,
      full_name: fullName,
    });
  }

  login(email: string, password: string) {
    return this.client.post('/api/v1/auth/login', {
      email,
      password,
    });
  }

  logout() {
    return this.client.post('/api/v1/auth/logout');
  }

  // Documents endpoints
  uploadDocument(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return this.client.post('/api/v1/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  listDocuments(page = 1, limit = 20) {
    return this.client.get('/api/v1/documents', {
      params: { page, limit },
    });
  }

  getDocument(documentId: string) {
    return this.client.get(`/api/v1/documents/${documentId}`);
  }

  deleteDocument(documentId: string) {
    return this.client.delete(`/api/v1/documents/${documentId}`);
  }

  getDocumentPreview(documentId: string) {
    return this.client.get(`/api/v1/documents/${documentId}/preview`);
  }

  // Chat endpoints
  chat(sessionId: string | null, query: string, documentIds: string[]) {
    return this.client.post('/api/v1/chat', {
      session_id: sessionId,
      query,
      document_ids: documentIds,
      stream: false,
    });
  }

  chatStream(sessionId: string | null, query: string, documentIds: string[]) {
    return this.client.post('/api/v1/chat/stream', {
      session_id: sessionId,
      query,
      document_ids: documentIds,
    }, {
      responseType: 'stream',
    });
  }

  getChatHistory(sessionId: string, limit = 50, offset = 0) {
    return this.client.get(`/api/v1/chat/history/${sessionId}`, {
      params: { limit, offset },
    });
  }

  createChatSession(title: string, documentIds: string[]) {
    return this.client.post('/api/v1/chat/sessions', {
      title,
      document_ids: documentIds,
    });
  }

  listChatSessions() {
    return this.client.get('/api/v1/chat/sessions');
  }

  deleteChatSession(sessionId: string) {
    return this.client.delete(`/api/v1/chat/sessions/${sessionId}`);
  }
}

export const apiClient = new APIClient();
