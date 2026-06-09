# Deploy to Vercel Now - Step by Step

Your credentials are ready! Follow these steps to deploy your app.

---

## 📦 Your Credentials (Ready to Use)

✅ All credentials are already configured in `backend/.env`
✅ No need to copy/paste - they're secure in the .env file

The following are already set:
- Hugging Face API Key
- Database URL (Supabase)
- Redis URL (Upstash)
- Gemini API Key

**Important:** Never commit `.env` to Git (it's in .gitignore)

---

## 🚀 Step 1: Install Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel (opens browser)
vercel login
# Choose: Continue with GitHub
```

---

## 🚀 Step 2: Deploy Backend

```bash
cd /root/ai-document-intelligence

# Create Vercel project
vercel link

# Answer prompts:
# - Scope: Your GitHub username
# - Project name: ai-document-intelligence-backend
# - Which directory: backend

# Deploy
vercel deploy --prod

# Copy the URL shown (example):
# https://ai-document-intelligence-backend-xxx.vercel.app
```

**Save your backend URL!**

---

## 🚀 Step 3: Add Environment Variables to Vercel

Go to: https://vercel.com/dashboard

1. Click on your project: `ai-document-intelligence-backend`
2. Go to: Settings → Environment Variables
3. Copy all values from your `backend/.env` file and add them:

```
Name: DATABASE_URL
Value: [from your .env file]

Name: REDIS_URL
Value: [from your .env file]

Name: GEMINI_API_KEY
Value: [from your .env file]

Name: HUGGINGFACE_API_KEY
Value: [from your .env file]

Name: JWT_SECRET
Value: [from your .env file]

Name: ENVIRONMENT
Value: production

Name: DEBUG
Value: False
```

**Tip:** Open `backend/.env` in your editor and copy each value

---

## 🚀 Step 4: Redeploy Backend

After adding environment variables:

```bash
# In backend directory
vercel deploy --prod --yes
```

Your backend is now live! ✨

---

## 🌐 Step 5: Deploy Frontend

```bash
cd ../frontend

# Create .env.local
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=https://your-backend-url-here.vercel.app
EOF

# Replace "your-backend-url-here" with your actual backend URL

# Deploy frontend
vercel deploy --prod

# Copy the frontend URL shown
```

**Your app is now live!** 🎉

---

## ✅ Step 6: Test Your App

### Test Backend
```bash
curl https://your-backend-url.vercel.app/health
# Should return: {"status":"healthy"}
```

### Test Frontend
```
Open: https://your-frontend-url.vercel.app
Register with email/password
Upload a PDF or text file
Ask a question
Get answer from Gemini!
```

---

## 📋 Troubleshooting

### Issue: "Database connection error"
**Solution:**
1. Check DATABASE_URL is correct in Vercel env vars
2. Go to Supabase → Settings → Network → Unblock Vercel IP
3. Redeploy: `vercel deploy --prod`

### Issue: "Redis connection timeout"
**Solution:**
1. Check REDIS_URL in Vercel env vars
2. Upstash uses TLS, which should work automatically
3. Check Upstash dashboard to ensure database is active

### Issue: "Embeddings API error"
**Solution:**
1. Check HUGGINGFACE_API_KEY is correct
2. Hugging Face free tier has rate limits
3. Wait a few seconds between requests

### Issue: "Frontend can't reach backend"
**Solution:**
1. Check NEXT_PUBLIC_API_URL in .env.local
2. Must start with https://
3. No trailing slash
4. Redeploy frontend: `vercel deploy --prod`

---

## 🎯 Your URLs

After deployment, you'll have:

```
Frontend: https://ai-document-intelligence-xxx.vercel.app
Backend API: https://ai-document-intelligence-backend-xxx.vercel.app
API Docs: https://ai-document-intelligence-backend-xxx.vercel.app/docs
```

---

## 💡 Pro Tips

1. **Save your URLs** - You'll need them for the frontend config
2. **Monitor Usage** - Vercel Dashboard shows request count and errors
3. **Check Logs** - `vercel logs` to debug issues
4. **Custom Domain** - Add your domain: `vercel domains add yourdomain.com`
5. **Auto Deploy** - Connect GitHub for auto-deploy on push

---

## 📊 Free Tier Status

```
Vercel Functions: 100 invocations included, then $0.50 per 1M
Supabase: 500MB storage, unlimited API calls
Upstash: 10,000 commands/day free
Hugging Face: Unlimited API calls
Gemini: 60 calls/minute free

For your testing: ALL FREE! ✨
```

---

## 🎉 Success Checklist

- [ ] Backend deployed to Vercel
- [ ] Environment variables added
- [ ] Frontend deployed to Vercel
- [ ] .env.local configured with backend URL
- [ ] Backend health check works (`/health`)
- [ ] Frontend loads at https://xxx.vercel.app
- [ ] Can register new user
- [ ] Can upload document
- [ ] Can ask question and get answer

---

## ⚠️ Important Reminders

1. **Never share API keys** - They're in .env but not in GitHub (safe)
2. **Keep credentials secure** - Don't paste them in chat
3. **Monitor rate limits** - Gemini: 60/min, HF: unlimited, Redis: 10K/day
4. **Test thoroughly** - Start with small documents
5. **Monitor free tier usage** - Watch your Supabase and Upstash dashboards

---

## 🚀 Next Steps After Deployment

1. **Share your app** - Give frontend URL to friends/users
2. **Get feedback** - Test with real documents
3. **Monitor performance** - Check Vercel logs for errors
4. **Upgrade if needed** - Switch to paid tier if you hit limits

---

## 📞 Need Help?

1. Check logs: `vercel logs --project ai-document-intelligence-backend`
2. Check Vercel dashboard for error details
3. Check Supabase/Upstash dashboards for connection issues
4. Review DEPLOY_VERCEL_NOW.md (this file) for troubleshooting

---

**Your AI Document Intelligence Platform is ready to deploy!** 🚀

Start with Step 1 above and follow through. You'll have a live app in 15-20 minutes!
