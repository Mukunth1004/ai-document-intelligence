# Quick Start: Deploy to Vercel in 30 Minutes

## ⚡ TL;DR

```bash
# 1. Get Hugging Face token (5 min)
# 2. Setup Supabase & Upstash (5 min)
# 3. Deploy with Vercel CLI (10 min)
# 4. Test your app (10 min)
```

**Total time: 30 minutes**

---

## 📋 Pre-requisites

- [ ] Node.js 18+ installed
- [ ] GitHub account
- [ ] This repo cloned locally

---

## 🔑 Step 1: Get API Keys (10 minutes)

### Hugging Face Token
1. Go: https://huggingface.co/settings/tokens
2. Create new token
3. Copy token → **Save as `HF_TOKEN`**

### Supabase Database URL
1. Go: https://supabase.com → Sign up with GitHub
2. Create project: `ai-document-intelligence`
3. Wait 2-3 minutes
4. Settings → Database → Connection Pooling
5. Copy URL → **Save as `DATABASE_URL`**
   - Make sure to add `+asyncpg`: `postgresql+asyncpg://...`

### Upstash Redis URL
1. Go: https://console.upstash.com → Sign up
2. Create Redis database
3. Copy Redis URL → **Save as `REDIS_URL`**

### Gemini API Key (You Already Have ✅)
```
AQ.Ab8RN... (your key)
```
Go to: https://ai.google.dev/ to get your key if needed

---

## 🚀 Step 2: Deploy (15 minutes)

### Install Vercel CLI
```bash
npm install -g vercel
vercel login  # Sign up with GitHub
```

### Deploy Backend
```bash
cd backend

# Create production env file
cat > .env.production << EOF
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=YOUR_SUPABASE_URL
REDIS_URL=YOUR_UPSTASH_URL
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
HUGGINGFACE_API_KEY=YOUR_HF_TOKEN
JWT_SECRET=$(openssl rand -base64 32)
EOF

# Deploy
vercel deploy --prod
```

**Note:** Copy your backend URL from output

### Deploy Frontend
```bash
cd ../frontend

# Update API URL
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
EOF

# Deploy
vercel deploy --prod
```

### Add Environment Variables to Vercel
```bash
cd ../backend

# Add each variable
vercel env add DATABASE_URL
vercel env add REDIS_URL  
vercel env add GEMINI_API_KEY
vercel env add HUGGINGFACE_API_KEY
vercel env add JWT_SECRET

# Redeploy
vercel deploy --prod
```

---

## ✅ Step 3: Test (5 minutes)

### Health Check
```bash
curl https://your-backend.vercel.app/health
```

### Access Frontend
Open: `https://your-frontend.vercel.app`

### Try It Out
1. Register with email/password
2. Upload a PDF or text file
3. Ask a question
4. Get answer from Gemini! ✨

---

## 🎯 Your URLs

| Component | URL |
|-----------|-----|
| Frontend | `https://your-frontend-xxx.vercel.app` |
| Backend | `https://your-backend-xxx.vercel.app` |
| API Docs | `https://your-backend-xxx.vercel.app/docs` |

---

## ⚠️ Common Issues

### "HUGGINGFACE_API_KEY not set"
```bash
vercel env add HUGGINGFACE_API_KEY
# Paste your HF token
vercel deploy --prod
```

### "Database connection error"
1. Check Supabase is running
2. Check DATABASE_URL is correct
3. Supabase → Settings → Network → Disable filtering

### "Embeddings timeout"
- Hugging Face free tier is slow
- Wait a few seconds between requests
- Or upgrade HF to paid

---

## 💰 Cost

```
Vercel: $0 (free tier)
Supabase: $0 (free tier)
Upstash: $0 (free tier)
Hugging Face: $0 (free tier)
Gemini: $0 (free tier)

TOTAL: $0/month 🎉
```

---

## 📞 More Help

See detailed guide: [VERCEL_SETUP.md](./VERCEL_SETUP.md)

---

**You're done! Your app is live! 🚀**
