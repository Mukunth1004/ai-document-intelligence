# Deploy Monorepo to Vercel (Best Approach)

Deploy both frontend and backend from a single repository on Vercel.

---

## 🎯 What is This?

This deploys your entire project (frontend + backend) as a single Vercel project:

```
https://your-project.vercel.app        ← Frontend (Next.js)
https://your-project.vercel.app/_/backend/api/v1/...  ← Backend (FastAPI)
```

**Advantages:**
- ✅ Single project to manage
- ✅ Single domain
- ✅ Automatic deployments on git push
- ✅ Free tier friendly
- ✅ No CORS issues (same domain)

---

## 🚀 Step 1: Connect GitHub to Vercel

1. Go to: https://vercel.com/dashboard
2. Click: "Add New..." → "Project"
3. Click: "Import Git Repository"
4. Select: `ai-document-intelligence`
5. Click: "Import"

---

## 🚀 Step 2: Configure Project Settings

On the "Configure Project" screen:

### Framework Preset
- Select: **Next.js**

### Build & Development Settings
- Keep defaults (Vercel auto-detects)

### Root Directory
- Leave empty (monorepo at root)

### Environment Variables
Click "Add Environment Variable" and add each from your `backend/.env`:

```
DATABASE_URL = [from your .env file]

REDIS_URL = [from your .env file]

GEMINI_API_KEY = [from your .env file]

HUGGINGFACE_API_KEY = [from your .env file]

JWT_SECRET = [from your .env file]

ENVIRONMENT = production

DEBUG = False

NEXT_PUBLIC_API_URL = //_/backend
```

**Important:** 
- Copy values from your local `backend/.env` file
- `NEXT_PUBLIC_API_URL` should be `//_/backend` (relative URL on Vercel)
- Local development uses: `http://localhost:3000/_/backend`

---

## 🚀 Step 3: Deploy

Click: "Deploy"

Vercel will:
1. Clone your repo
2. Install dependencies
3. Build frontend (Next.js)
4. Build backend (Python)
5. Deploy everything
6. Give you your URL

---

## ✅ Step 4: Verify Deployment

After deployment completes:

### Test Backend Health
```bash
curl https://your-project.vercel.app/_/backend/health
# Should return: {"status":"healthy"}
```

### Test Frontend
```bash
# Visit: https://your-project.vercel.app
# Should load homepage
```

### Test Full Flow
1. Open: https://your-project.vercel.app
2. Register with email/password
3. Upload a PDF document
4. Ask a question
5. Get answer from Gemini! ✨

---

## 🔄 Automatic Deployments

After initial deploy:

```bash
# Push to GitHub
git push origin main

# Vercel automatically:
# 1. Detects the push
# 2. Builds frontend & backend
# 3. Deploys new version
# 4. Updates live site
```

No more manual deployment commands! 🎉

---

## 📁 Project Structure on Vercel

```
your-project.vercel.app/
├── /                           ← Frontend (Next.js)
│   ├── /auth/login            ← Login page
│   ├── /auth/register         ← Register page
│   ├── /dashboard             ← Dashboard
│   └── /dashboard/documents/  ← Document chat
│
└── /_/backend/                ← Backend (FastAPI)
    ├── /api/v1/auth/register
    ├── /api/v1/auth/login
    ├── /api/v1/documents/upload
    ├── /api/v1/chat
    ├── /health
    └── /docs                  ← API documentation
```

---

## 🛠️ Making Changes

After deployment, making changes is easy:

```bash
# Make a code change
# (e.g., update backend or frontend)

# Commit and push
git add .
git commit -m "Your changes"
git push origin main

# Vercel automatically redeploys!
# Check deployment at: https://vercel.com/dashboard
```

---

## 📊 Your URLs

```
🌐 Frontend: https://your-project.vercel.app
📚 API Docs: https://your-project.vercel.app/_/backend/docs
🔗 Backend: https://your-project.vercel.app/_/backend/api/v1/...
```

---

## 🐛 Troubleshooting

### Issue: "Build failed"
**Solution:**
1. Check Vercel logs: https://vercel.com/dashboard → your project → "Deployments"
2. Look for error details
3. Common issues:
   - Missing environment variable
   - Database connection error
   - Python dependency error

### Issue: "Cannot reach backend"
**Solution:**
1. Check frontend `.env.local` has: `NEXT_PUBLIC_API_URL=//_/backend`
2. Or local: `http://localhost:3000/_/backend`
3. No trailing slash!
4. Redeploy frontend

### Issue: "Database connection timeout"
**Solution:**
1. Verify DATABASE_URL is correct in Vercel env vars
2. Check Supabase database is active
3. Go to Supabase → Network → allow Vercel's IP

### Issue: "Redis connection error"
**Solution:**
1. Verify REDIS_URL is correct
2. Check Upstash database is running
3. Test connection in Upstash dashboard

---

## 💡 Environment Variables

Local development (`.env`):
```
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...
NEXT_PUBLIC_API_URL=http://localhost:3000/_/backend
```

Production (Vercel Dashboard):
```
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...
NEXT_PUBLIC_API_URL=//_/backend
```

**Note:** `NEXT_PUBLIC_API_URL` is different for local vs production!

---

## 🔐 Security

```
✅ .env file: NOT in Git (it's in .gitignore)
✅ Vercel Secrets: Stored encrypted in Vercel
✅ No credentials in code
✅ HTTPS only (Vercel automatic)
✅ CORS configured
```

---

## 📈 Monitoring

### Vercel Dashboard
- Go to: https://vercel.com/dashboard
- Click your project
- See:
  - Build logs
  - Deployment history
  - Analytics
  - Error logs

### Real-time Logs
```bash
# Watch logs in real-time
vercel logs --follow
```

---

## 🚀 Advanced: Custom Domain

To add your own domain:

1. Go to Vercel Dashboard → Your Project → Settings
2. Domains → Add Domain
3. Configure DNS at your registrar
4. Verify domain
5. Your app now at: https://yourdomain.com

---

## 💰 Costs

```
Vercel: Free tier (included)
Supabase: Free tier ($0)
Upstash: Free tier ($0)
Hugging Face: Free tier ($0)
Gemini: Free tier ($0)

TOTAL: $0/month 🎉
```

---

## ✅ Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] Vercel project created and linked
- [ ] All environment variables added
- [ ] Initial deployment completed
- [ ] Backend `/health` responds
- [ ] Frontend loads
- [ ] Can register and login
- [ ] Can upload document
- [ ] Can ask questions
- [ ] Getting answers from Gemini

---

## 📞 Need Help?

1. **Check Vercel Logs:**
   - Dashboard → Your Project → "Deployments" → Latest → "Logs"

2. **Check GitHub Actions:**
   - Repo → "Actions" tab → See deployment status

3. **Common Issues:**
   - Database/Redis connection → Check env vars
   - Build failure → Check logs for Python errors
   - Frontend not loading → Check build output

4. **Reset Everything:**
   ```bash
   # Pull latest from GitHub
   git pull origin main
   
   # Redeploy on Vercel
   # Go to Dashboard → Deployments → Redeploy
   ```

---

## 🎓 What Happens on Deploy

```
1. Git push detected
   ↓
2. Vercel clones repo
   ↓
3. Install Python deps (backend)
   ↓
4. Install Node deps (frontend)
   ↓
5. Build Next.js (frontend)
   ↓
6. Configure FastAPI (backend)
   ↓
7. Deploy all at once
   ↓
8. Your app is live!
```

**Total time: 3-5 minutes**

---

## 🎉 You're Done!

Your app is now deployed on Vercel with:
- ✅ Frontend at `/`
- ✅ Backend at `/_/backend`
- ✅ Single domain
- ✅ Automatic deployments
- ✅ Zero cost

Just push to GitHub and Vercel deploys automatically! 🚀

---

## 📚 Next Steps

1. Share your URL with friends
2. Test with real documents
3. Monitor performance in Vercel Dashboard
4. Add custom domain (optional)
5. Upgrade to paid tier if needed (optional)

**Your AI Document Intelligence Platform is LIVE!** 🎉
