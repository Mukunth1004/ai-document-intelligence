# Monorepo Structure Guide

Your project is organized as a monorepo with frontend and backend in a single repository.

---

## 📁 Project Structure

```
ai-document-intelligence/
│
├── frontend/                    ← Next.js React app
│   ├── app/                    ← App directory (Next.js 13+)
│   ├── components/             ← React components
│   ├── lib/
│   │   ├── api.ts             ← Backend API client
│   │   └── hooks/             ← Custom React hooks
│   ├── .env.local             ← Local environment variables
│   ├── package.json
│   └── vercel.json (optional)
│
├── backend/                     ← FastAPI Python app
│   ├── app/
│   │   ├── main.py            ← FastAPI entry point
│   │   ├── config.py          ← Configuration
│   │   ├── models.py          ← Database models
│   │   ├── auth/              ← Authentication
│   │   ├── documents/         ← Document upload/processing
│   │   ├── chat/              ← Chat endpoints
│   │   └── rag/               ← RAG pipeline
│   ├── .env                   ← Environment variables (NOT in Git)
│   ├── requirements.txt
│   └── Dockerfile (optional)
│
├── vercel.json                ← Vercel deployment config
├── .gitignore                 ← Git ignore rules
└── README.md

```

---

## 🚀 Local Development

### Terminal 1: Start Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend runs at: `http://localhost:8000`

### Terminal 2: Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:3000`

### Frontend Communicates with Backend
- Local: `http://localhost:3000/_/backend/api/v1/...`
- Uses URL from: `frontend/.env.local`

---

## 🎯 Environment Variables

### Backend (`backend/.env`)
```env
# Database
DATABASE_URL=postgresql+asyncpg://...

# Cache
REDIS_URL=redis://...

# APIs
GEMINI_API_KEY=...
HUGGINGFACE_API_KEY=...

# Security
JWT_SECRET=...

# Settings
ENVIRONMENT=development
DEBUG=True
```

**Note:** This file is NOT in Git (safe from leaks)

### Frontend (`frontend/.env.local`)
```env
# Backend URL for local development
NEXT_PUBLIC_API_URL=http://localhost:3000/_/backend
```

**Note:** On Vercel, this becomes `//_/backend` (relative URL)

---

## 📡 API Communication Flow

### Local Development
```
Frontend (localhost:3000)
    ↓
api.ts client
    ↓
Backend (localhost:3000/_/backend)
    ↓
Database (Supabase)
Cache (Upstash)
LLM (Gemini)
```

### Production (Vercel)
```
Frontend (your-domain.vercel.app)
    ↓
api.ts client (uses //_/backend)
    ↓
Backend (//_/backend on same domain)
    ↓
Database (Supabase)
Cache (Upstash)
LLM (Gemini)
```

---

## 🔗 API Endpoints

All endpoints are prefixed with the backend route:

### Local
```
GET http://localhost:3000/_/backend/health
POST http://localhost:3000/_/backend/api/v1/auth/register
POST http://localhost:3000/_/backend/api/v1/auth/login
POST http://localhost:3000/_/backend/api/v1/documents/upload
```

### Production (Vercel)
```
GET https://your-domain.vercel.app/_/backend/health
POST https://your-domain.vercel.app/_/backend/api/v1/auth/register
POST https://your-domain.vercel.app/_/backend/api/v1/auth/login
```

---

## 🐛 Debugging

### Check Backend Health
```bash
curl http://localhost:3000/_/backend/health
# Or with local backend on 8000:
curl http://localhost:8000/health
```

### View API Documentation
```
Local: http://localhost:8000/docs
Production: https://your-domain.vercel.app/_/backend/docs
```

### Check Frontend Logs
```bash
# Browser console
F12 or Cmd+Option+I
Console tab
```

### Check Backend Logs
```bash
# Terminal where backend is running
Look for error messages
```

---

## 📦 Deploying Changes

### Update Backend
1. Make changes in `backend/`
2. Test locally: `uvicorn app.main:app --reload`
3. Commit: `git add . && git commit -m "..."`
4. Push: `git push origin main`
5. Vercel auto-deploys!

### Update Frontend
1. Make changes in `frontend/`
2. Test locally: `npm run dev`
3. Commit: `git add . && git commit -m "..."`
4. Push: `git push origin main`
5. Vercel auto-deploys!

### Update Both
1. Make changes in both directories
2. Test locally in both terminals
3. Commit all changes: `git add . && git commit -m "..."`
4. Push: `git push origin main`
5. Vercel builds and deploys everything!

---

## 🔄 Monorepo Benefits

### Single Repository
- ✅ One code repository
- ✅ One Git history
- ✅ Easier collaboration
- ✅ Single PR review

### Single Deployment
- ✅ One Vercel project
- ✅ Frontend and backend deploy together
- ✅ No CORS issues (same domain)
- ✅ Atomic deployments

### Better Development
- ✅ One setup process
- ✅ One `.env` file (backend)
- ✅ One deployment process
- ✅ Easy to maintain

---

## 🚀 Making Your First Change

### Example: Update Frontend

```bash
# 1. Make a change
# Edit: frontend/app/page.tsx
# Change the home page text

# 2. Test locally
cd frontend
npm run dev
# Visit http://localhost:3000
# See your change

# 3. Commit
git add frontend/app/page.tsx
git commit -m "Update homepage text"

# 4. Push
git push origin main

# 5. Vercel redeploys automatically!
# Check: https://vercel.com/dashboard
```

### Example: Update Backend

```bash
# 1. Make a change
# Edit: backend/app/rag/gemini_client.py
# Update the system prompt

# 2. Test locally
# Backend is running in other terminal
# It reloads automatically (--reload flag)

# 3. Test in frontend
# Frontend calls backend
# Test the new behavior

# 4. Commit
git add backend/app/rag/gemini_client.py
git commit -m "Update Gemini system prompt"

# 5. Push
git push origin main

# 6. Vercel redeploys backend automatically!
```

---

## 📊 Development Workflow

```
1. Create a branch (optional)
   git checkout -b feature/my-feature

2. Make changes in frontend/ or backend/

3. Test locally
   - Start both servers
   - Use the app
   - Check logs

4. Commit changes
   git add .
   git commit -m "Add new feature"

5. Push to GitHub
   git push origin main

6. Vercel auto-deploys
   - Builds frontend
   - Builds backend
   - Deploys both
   - Your app updates live

7. Verify on production
   - Visit: https://your-domain.vercel.app
   - Test the changes
```

---

## 🔐 Secrets & Security

### What NOT to commit
```
backend/.env          ← ❌ Credentials (Git ignored)
frontend/.env.local   ← ❌ Local only
.env.production       ← ❌ Never commit
credentials.json      ← ❌ Never commit
```

### What TO commit
```
backend/.env.example  ← ✅ Template only
frontend/.env.example ← ✅ Template only
vercel.json          ← ✅ Config (no secrets)
```

### Secrets on Vercel
1. Add to: Vercel Dashboard → Project → Settings → Environment Variables
2. They're encrypted at rest
3. Injected at build time
4. Never in your code

---

## 🎯 File Changes Decision Tree

```
Did you modify...

├── frontend files?
│   ├── app/         → Frontend change only
│   ├── components/  → Frontend change only
│   ├── lib/         → Frontend change only
│   └── .env.local   → Local only (don't commit)
│
├── backend files?
│   ├── app/         → Backend change only
│   ├── requirements.txt → Backend change
│   └── .env         → Local only (don't commit)
│
├── vercel.json?     → Deployment config
├── README.md?       → Documentation
├── .gitignore?      → Git config
│
└── Both frontend and backend?
    → Full stack changes
    → One commit, one deploy
```

---

## 💡 Tips

1. **Keep frontend and backend independent**
   - Can change either without breaking the other
   - Version them separately in commits

2. **Test changes locally first**
   - Start both servers
   - Use the application
   - Check logs

3. **Use meaningful commit messages**
   - Good: `"Add document upload with progress bar"`
   - Bad: `"Update stuff"`

4. **Commit together for related changes**
   - Example: API change + frontend UI change = one commit

5. **Use GitHub branches for big features**
   - Create branch: `git checkout -b feature/name`
   - Work on it
   - Push and create PR for review
   - Merge to main when done

---

## 🚀 Ready to Develop?

```bash
# Setup
git clone <your-repo>
cd ai-document-intelligence

# Terminal 1: Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev

# Visit: http://localhost:3000
# Start developing!
```

---

## 📞 Common Questions

**Q: Can I develop backend without frontend?**
A: Yes! Backend runs independently at `localhost:8000` with `/docs` for testing

**Q: Can I deploy just the frontend?**
A: Yes! Push changes to frontend/ and Vercel rebuilds just the frontend

**Q: What if backend deployment fails?**
A: Previous version stays live. Check Vercel logs to fix the issue and redeploy

**Q: How do I rollback a deployment?**
A: Vercel Dashboard → Deployments → Click previous version → "Redeploy"

**Q: Can I preview changes before deployment?**
A: Yes! Vercel creates preview deployments for pull requests

---

## 🎉 You're Ready!

Your monorepo is fully configured for:
- ✅ Local development
- ✅ Testing
- ✅ Automatic deployments
- ✅ Production readiness

Start developing! 🚀
