# Vercel Deployment Guide (100% Free)

This guide shows how to deploy the AI Document Intelligence Platform on Vercel completely free.

## 📊 Architecture

```
Vercel (Frontend + Backend) → Supabase (Database) → Upstash (Cache)
                            ↓
                     Hugging Face (Embeddings)
                            ↓
                      Gemini API (AI)
```

**Total Cost: $0/month** 💰

---

## 🔑 Step 1: Get Free API Keys

### 1.1 Google Gemini API Key
- Go to: https://ai.google.dev/
- Click "Get API Key"
- Create new project
- Copy key (format: `AIzaSy...` or `AQ.Ab8RN...`)
- **Note:** You have your own key, add it in environment variables

### 1.2 Hugging Face API Token
1. Go to: https://huggingface.co/settings/tokens
2. Create new token
3. Name: "ai-doc-intelligence"
4. Type: "Read"
5. Copy token (format: `hf_...`)
6. **Save this** - you'll need it

### 1.3 Supabase Database
1. Go to: https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub
4. Create new project:
   - Project name: `ai-document-intelligence`
   - Password: Create strong password
   - Region: Choose closest to you
5. Wait for setup (2-3 minutes)
6. Go to "Settings" → "Database" → "Connection Pooling"
7. Copy connection string (looks like):
   ```
   postgresql://[user]:[password]@[host]:6543/postgres
   ```
8. Update to async format:
   ```
   postgresql+asyncpg://[user]:[password]@[host]:6543/postgres
   ```

### 1.4 Upstash Redis
1. Go to: https://console.upstash.com
2. Sign up with GitHub
3. Create new Redis database:
   - Name: `ai-doc-intelligence`
   - Region: Global
4. Copy Redis URL (looks like):
   ```
   redis://default:[password]@[host]:6379
   ```

---

## 🚀 Step 2: Deploy Backend to Vercel

### 2.1 Install Vercel CLI
```bash
npm install -g vercel
```

### 2.2 Login to Vercel
```bash
vercel login
# Opens browser, sign up with GitHub
```

### 2.3 Configure Environment Variables

Create `backend/.env.production`:
```env
ENVIRONMENT=production
DEBUG=False

DATABASE_URL=postgresql+asyncpg://[user]:[password]@[host]:6543/postgres
REDIS_URL=redis://default:[password]@[host]:6379

JWT_SECRET=generate-a-long-random-string-here
GEMINI_API_KEY=your-gemini-api-key-here
HUGGINGFACE_API_KEY=hf_your_token_here

CHUNK_SIZE=1024
CHUNK_OVERLAP=204
SIMILARITY_THRESHOLD=0.6
TOP_K_CHUNKS=10
```

### 2.4 Deploy Backend
```bash
cd backend
vercel deploy --prod

# Follow prompts:
# - Connect to GitHub? Yes
# - Project name: ai-document-intelligence-backend
# - Framework: Other
```

**Get your backend URL:** `https://ai-document-intelligence-backend-xxx.vercel.app`

### 2.5 Add Environment Variables to Vercel
```bash
vercel env add DATABASE_URL
# Paste: postgresql+asyncpg://[user]:[password]@[host]:6543/postgres

vercel env add REDIS_URL
# Paste: redis://default:[password]@[host]:6379

vercel env add JWT_SECRET
# Paste: your-long-random-secret-key

vercel env add GEMINI_API_KEY
# Paste: your Gemini API key

vercel env add HUGGINGFACE_API_KEY
# Paste: hf_your_token_here
```

---

## 🌐 Step 3: Deploy Frontend to Vercel

### 3.1 Create `.env.local`
```bash
cd frontend
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=https://ai-document-intelligence-backend-xxx.vercel.app
EOF
```

### 3.2 Deploy Frontend
```bash
vercel deploy --prod

# Follow prompts:
# - Connect to GitHub? Yes
# - Project name: ai-document-intelligence
# - Framework: Next.js
```

**Get your frontend URL:** `https://ai-document-intelligence-xxx.vercel.app`

---

## 📝 Step 4: Setup Database Schema

### 4.1 Create Database Tables

Option A: Using Supabase UI
```sql
-- Go to Supabase Console → SQL Editor
-- Create new query
-- Copy the schema from backend/migrations or the SQL schema provided
```

Option B: Using migrations
```bash
cd backend
alembic upgrade head
```

---

## ✅ Step 5: Verification

### Test 1: Health Check
```bash
curl https://your-backend.vercel.app/health
# Expected: {"status":"healthy"}
```

### Test 2: Register User
```bash
curl -X POST https://your-backend.vercel.app/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### Test 3: Access Frontend
- Open: `https://your-frontend.vercel.app`
- Register and login
- Upload a document
- Ask a question

---

## 🎯 Using Your App

1. **Frontend:** `https://your-frontend.vercel.app`
2. **Backend API:** `https://your-backend.vercel.app`
3. **API Docs:** `https://your-backend.vercel.app/docs`

---

## 📊 Free Tier Limits

| Service | Limit | Usage |
|---------|-------|-------|
| **Vercel** | 1000 serverless functions | OK for small projects |
| **Supabase** | 500MB storage, unlimited API | OK for ~1000 documents |
| **Upstash** | 10,000 commands/day | ~330/hour (OK) |
| **Hugging Face** | Free tier | Unlimited |
| **Gemini** | 60 calls/minute | OK for testing |

**These limits are sufficient for personal/testing use!**

---

## 🐛 Troubleshooting

### Issue: "HUGGINGFACE_API_KEY not set"
**Solution:**
```bash
vercel env add HUGGINGFACE_API_KEY
# Paste your Hugging Face token
vercel deploy --prod
```

### Issue: "Database connection error"
**Solution:**
1. Check Supabase database is running
2. Verify DATABASE_URL is correct
3. Go to Supabase → Network → Add Vercel IP to allowlist
4. Check connection string format

### Issue: "Embeddings timeout"
**Solution:**
- Hugging Face free tier has rate limits
- Wait between requests
- Or upgrade to paid Hugging Face plan

### Issue: "Redis connection failed"
**Solution:**
1. Check Upstash database is active
2. Verify REDIS_URL is correct
3. Test connection: `redis-cli ping`

---

## 🚀 Advanced: Custom Domain

### Add Custom Domain
```bash
vercel domains add yourdomain.com

# Verify DNS:
vercel domains verify yourdomain.com

# Set as primary:
vercel domains set yourdomain.com
```

---

## 📈 Monitoring

### Vercel Analytics
- Dashboard: https://vercel.com/dashboard
- See request count, response times, errors

### Supabase Monitoring
- Dashboard: https://app.supabase.com
- See database usage, queries, connections

### Upstash Monitoring
- Dashboard: https://console.upstash.com
- See Redis usage, commands/day

---

## 💡 Tips

1. **Save your API keys** in a secure place
2. **Use environment variables** never commit secrets
3. **Monitor free tier usage** to avoid surprises
4. **Test locally first** before pushing to Vercel
5. **Use Vercel preview deployments** for testing

---

## 🎓 Environment Variables Checklist

- [ ] GEMINI_API_KEY - Your Gemini key
- [ ] HUGGINGFACE_API_KEY - Your Hugging Face token
- [ ] DATABASE_URL - Your Supabase connection
- [ ] REDIS_URL - Your Upstash connection
- [ ] JWT_SECRET - Random 32+ char string

---

## 📞 Support

If you run into issues:
1. Check logs: `vercel logs`
2. Check Supabase console for errors
3. Check Upstash dashboard for connection issues
4. Check Hugging Face API status

---

**Your app is now live on Vercel, completely free!** 🎉
