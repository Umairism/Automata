# 🚀 Quick Deploy to Railway.app

## 1️⃣ Push to GitHub
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

## 2️⃣ Deploy on Railway (3 Minutes!)

1. Go to **[railway.app](https://railway.app)** and sign up (FREE)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your **`Automata`** repository
5. Railway **auto-detects** everything:
   - ✅ Python 3.11
   - ✅ Flask framework
   - ✅ Port 8080 (pre-configured)
   - ✅ Dependencies
6. Wait 3-5 minutes ⏳
7. **Done!** Your app is live 🎉

## 3️⃣ Your Live URL
`https://automata-solver-production.up.railway.app` (or your custom name)

---

## Alternative: Render.com

If you prefer Render:
1. Go to **[render.com](https://render.com)**
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub → Select `Automata`
4. Configure:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Type: Free
5. Wait 5-10 minutes

---

## Why Not Netlify?

Netlify only hosts **static sites** (HTML/CSS/JS). Your Automata Solver uses **Flask** (Python backend), which needs a server to run. That's why we use **Railway** or **Render** instead.

**Netlify = Static files only**
**Railway/Render = Static + Backend (Perfect for your app!)**

---

## Need Help?

See full guide: **[DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md)**
