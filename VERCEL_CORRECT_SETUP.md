# Correct Vercel Setup (Fixed Runtime Issue)

This guide shows the correct way to deploy your monorepo to Vercel.

---

## ✅ What's Fixed

```
❌ Old: "Function Runtimes must have a valid version"
✅ New: Proper Python runtime configuration
```

The project now uses:
- **Frontend**: Next.js at `/`
- **Backend**: Python FastAPI at `/_/backend`
- **API Handler**: `backend/api/index.py` (Vercel-compatible)

---

## 🚀 Step 1: Verify Local Structure

Your project should have:

```
ai-document-intelligence/
├── frontend/              ← Next.js app
│   ├── app/
│   ├── lib/
│   └── .env.local         ← Has NEXT_PUBLIC_API_URL
│
├── backend/
│   ├── api/
│   │   └── index.py       ← ✅ New Vercel entry point
│   └── app/
│       └── main.py        ← FastAPI app
│
└── vercel.json            ← ✅ Updated configuration
```

---

## 🚀 Step 2: Deploy to Vercel

### Option A: Connect GitHub (Easiest) ⭐

1. **Go to:** https://vercel.com/dashboard
2. **Click:** "Add New..." → "Project"
3. **Select:** "Import Git Repository"
4. **Choose:** `ai-document-intelligence`
5. **Click:** "Import"

### Option B: Use Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

---

## 🚀 Step 3: Configure Environment Variables

**In Vercel Dashboard:**

1. Click your project
2. Go to: **Settings** → **Environment Variables**
3. Add these variables:

```
DATABASE_URL
Your PostgreSQL connection string

REDIS_URL  
Your Redis connection string

GEMINI_API_KEY
Your Gemini API key

HUGGINGFACE_API_KEY
Your Hugging Face token

JWT_SECRET
A random 32+ character secret

ENVIRONMENT
production

DEBUG
False

NEXT_PUBLIC_API_URL
(Leave empty - uses default /_/backend)
```

---

## 🚀 Step 4: Deploy

**Click:** "Deploy"

Vercel will:
1. ✅ Detect Next.js framework
2. ✅ Build frontend
3. ✅ Install Python dependencies
4. ✅ Configure backend API
5. ✅ Deploy everything

**Wait 3-5 minutes...**

---

## ✅ Step 5: Test Deployment

### Test Backend Health
```bash
curl https://your-project.vercel.app/_/backend/health
# Expected: {"status":"healthy"}
```

### Test Frontend
```
Visit: https://your-project.vercel.app
Should load homepage
```

### Test Full Flow
1. Register with email/password
2. Upload a PDF
3. Ask a question
4. Get answer from Gemini! ✨

---

## 📊 URL Structure

```
https://your-project.vercel.app/
├── /                           ← Frontend homepage
├── /auth/login                ← Login page
├── /auth/register             ← Register page
├── /dashboard                 ← Dashboard
└── /_/backend/                ← Backend API
    ├── /health                ← Health check
    ├── /docs                  ← API documentation
    ├── /api/v1/auth/register  ← Auth endpoints
    ├── /api/v1/auth/login
    ├── /api/v1/documents/upload
    ├── /api/v1/chat
    └── ... (all endpoints)
```

---

## 🔄 Making Updates

After deployment, updating is simple:

```bash
# Make changes to frontend or backend
# Commit and push
git add .
git commit -m "Your changes"
git push origin main

# Vercel automatically:
# 1. Detects the push
# 2. Builds both frontend and backend
# 3. Deploys everything
# 4. Updates your live site

# Done! No manual deployment needed!
```

---

## 🐛 Troubleshooting

### Issue: "Build failed"
**Solution:**
1. Check Vercel logs: Dashboard → Deployments → Click latest
2. Look for error details
3. Common causes:
   - Missing environment variable
   - Python package import error
   - Database connection issue

### Issue: "Cannot reach backend from frontend"
**Solution:**
1. Check `NEXT_PUBLIC_API_URL` is not set (uses default)
2. Or set to `//_/backend` for production
3. Frontend should call `/_/backend` on Vercel
4. Redeploy frontend: Dashboard → Deployments → Redeploy

### Issue: "Database connection timeout"
**Solution:**
1. Verify DATABASE_URL is correct
2. Check Supabase network settings
3. Allow Vercel's IP in Supabase firewall
4. Test connection: `psql $DATABASE_URL -c "SELECT 1"`

### Issue: "Python import error"
**Solution:**
1. Check all packages are in `requirements.txt`
2. Verify `backend/api/index.py` exists
3. Check logs for specific missing module
4. Add missing package to requirements.txt
5. Redeploy

### Issue: "Redis connection failed"
**Solution:**
1. Verify REDIS_URL is correct
2. Test in Upstash dashboard
3. Check it's not expired
4. Create new Redis if needed

---

## 📁 Key Files

### `vercel.json`
Tells Vercel how to build and deploy:
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/.next",
  "framework": "nextjs"
}
```

### `backend/api/index.py`
Entry point for backend on Vercel:
```python
from app.main import app
handler = app
```

### `frontend/.env.local`
Local development API URL:
```
NEXT_PUBLIC_API_URL=http://localhost:3000/_/backend
```

---

## 🔐 Security

```
✅ .env file: NOT in Git (ignored)
✅ Vercel Secrets: Encrypted storage
✅ No credentials in code
✅ HTTPS by default
✅ CORS configured
```

---

## 💡 How It Works on Vercel

```
1. User visits: https://your-project.vercel.app

2. Vercel serves Next.js frontend

3. Frontend needs data, calls: /_/backend/api/v1/...

4. Vercel routes to: backend/api/index.py

5. Python FastAPI app processes request

6. Calls database, cache, LLM

7. Returns response to frontend

8. User sees result!
```

---

## 📊 File Tree (Important Parts)

```
.
├── vercel.json               ✅ Deployment config
├── frontend/
│   ├── .env.local            ← Local dev only
│   ├── app/page.tsx
│   ├── lib/api.ts            ← Calls /_/backend
│   └── package.json
└── backend/
    ├── api/
    │   └── index.py          ✅ Vercel entry point
    ├── app/
    │   ├── main.py           ← FastAPI app
    │   ├── config.py
    │   ├── models.py
    │   └── ...
    └── requirements.txt
```

---

## ✅ Deployment Checklist

- [ ] Project code pushed to GitHub
- [ ] `backend/api/index.py` exists
- [ ] `vercel.json` updated
- [ ] Connected to Vercel (GitHub integration)
- [ ] Added all environment variables
- [ ] Deployment completed (3-5 min)
- [ ] Backend `/health` responds
- [ ] Frontend loads
- [ ] Can register and login
- [ ] Can upload document
- [ ] Can ask and get answers

---

## 🎯 Expected URLs

After successful deployment:

```
🌐 Homepage:    https://your-project.vercel.app
🔗 Dashboard:   https://your-project.vercel.app/dashboard
📚 API Docs:    https://your-project.vercel.app/_/backend/docs
✨ Live App:    Ready to use!
```

---

## 📞 Common Questions

**Q: Do I need to run the backend separately?**
A: No! Vercel handles it. Just connect GitHub and deploy.

**Q: Will automatic deployments work?**
A: Yes! Push to main → Vercel auto-builds and deploys.

**Q: Can I test locally first?**
A: Yes! Use `npm run dev` for frontend and `uvicorn` for backend.

**Q: What if deployment fails?**
A: Check Vercel logs for errors, fix, and redeploy.

**Q: Can I add a custom domain?**
A: Yes! Vercel Dashboard → Domains → Add Domain

---

## 🚀 You're Ready!

Your monorepo is properly configured for Vercel.

**Next Steps:**
1. Go to https://vercel.com/dashboard
2. Connect your GitHub repo
3. Add environment variables
4. Click "Deploy"
5. Wait 3-5 minutes
6. Your app is live! 🎉

---

**Everything is set up correctly now!** 🎉
