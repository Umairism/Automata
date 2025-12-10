# 🚂 Railway Deployment Guide

## Quick Deploy to Railway.app

Your Automata Solver is configured for Railway deployment with port 8080.

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Configure for Railway deployment"
git push origin main
```

### Step 2: Deploy on Railway

1. **Go to [railway.app](https://railway.app)** and sign up

2. **Click "New Project"**

3. **Select "Deploy from GitHub repo"**

4. **Choose your `Automata` repository**

5. **Railway will auto-detect:**
   - ✅ Python environment
   - ✅ Flask framework
   - ✅ Dependencies from requirements.txt
   - ✅ Port configuration (PORT=8080)

6. **Wait 3-5 minutes** for deployment

7. **Get your URL** from Railway dashboard

### Step 3: Configure (Optional)

Railway auto-configures everything, but you can verify:

**Environment Variables:**
- `PORT` - Auto-set by Railway (usually 8080)
- `PYTHON_VERSION` - Auto-detected from runtime.txt
- `FLASK_ENV` - Set to `production` (optional)

**Settings:**
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Build Command**: `pip install -r requirements.txt`

### Step 4: Done! 🎉

Your app is live at: `https://automata-solver-production.up.railway.app`

---

## Railway Configuration Files

Your project includes:

- ✅ **`Procfile`** - Process configuration (gunicorn with $PORT)
- ✅ **`nixpacks.toml`** - Nixpacks configuration for Railway
- ✅ **`runtime.txt`** - Python version (3.11.6)
- ✅ **`requirements.txt`** - Python dependencies

---

## Port Configuration

Your `app.py` is configured to:
- Use **port 8080** by default (Railway standard)
- Read from `PORT` environment variable
- Bind to `0.0.0.0` for external access

```python
port = int(os.environ.get('PORT', 8080))
app.run(host='0.0.0.0', port=port)
```

---

## Railway vs Other Platforms

| Platform | Default Port | Cost | Setup Time |
|----------|--------------|------|------------|
| **Railway** | 8080 | FREE ($5 credit/mo) | 3 minutes |
| Render | Auto | FREE (750 hrs/mo) | 5 minutes |
| Vercel | Auto | FREE | 2 minutes |
| Heroku | Auto | $7/month | 5 minutes |

---

## Troubleshooting

### Port Issues
If you see "port already in use":
- Railway automatically sets `PORT` environment variable
- Your app reads `PORT` from environment
- No manual configuration needed

### Build Fails
Check Railway logs:
```bash
# View in Railway dashboard
Settings → Deployments → View Logs
```

Common fixes:
- Ensure `requirements.txt` is committed
- Check Python version in `runtime.txt`
- Verify all imports in `app.py`

### App Won't Start
1. Check start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
2. Verify gunicorn is in `requirements.txt` ✅
3. Check Railway logs for errors

### CORS Errors
- Flask-CORS is installed ✅
- CORS(app) is enabled in app.py ✅
- Should work automatically

---

## Railway Features You Get

✅ **Auto-deployment** - Push to GitHub = Auto deploy
✅ **Custom domains** - Connect your own domain
✅ **Environment variables** - Easy configuration
✅ **Logs & monitoring** - Real-time logs
✅ **Preview deployments** - Test before merging
✅ **Database support** - Add PostgreSQL/MySQL easily
✅ **Instant rollback** - Revert to previous version

---

## Cost & Limits

**FREE Tier ($5 credit/month):**
- ~500 hours of runtime
- Perfect for personal/academic projects
- No credit card required initially
- Unused credit doesn't roll over

**Paid Plans:**
- Start at $5/month
- Pay for what you use
- No cold starts
- Higher limits

---

## Testing Your Deployment

After deployment, test all features:

### Quick Test Checklist:
- [ ] App loads without errors
- [ ] DFA examples work (4 tests)
- [ ] NFA examples work (3 tests)
- [ ] PDA examples work (4 tests)
- [ ] CFG examples work (5 tests)
- [ ] TM examples work (4 tests)
- [ ] Theory examples work (5 tests)
- [ ] Diagrams render correctly
- [ ] No CORS errors in console

---

## Pro Tips

### 1. Custom Domain
```
Settings → Networking → Custom Domain
Add: automata.yourdomain.com
```

### 2. View Logs
```
Deployments → Latest → View Logs
Monitor real-time requests and errors
```

### 3. Environment Variables
```
Variables → Add Variable
Example: FLASK_ENV=production
```

### 4. Auto-Deploy
Railway auto-deploys when you push to main:
```bash
git add .
git commit -m "Update feature"
git push origin main
# Deploys automatically! 🚀
```

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy on Railway
3. ✅ Test all features
4. ✅ Share your live URL
5. ⭐ Star the repository (optional)

---

## Support

**Railway Documentation:** https://docs.railway.app
**Your Project Dashboard:** https://railway.app/dashboard

**Common Commands:**
```bash
# Install Railway CLI (optional)
npm i -g @railway/cli

# Login
railway login

# Deploy from CLI
railway up

# View logs
railway logs
```

---

## Success! 🎉

Your Automata Solver is live on Railway with:
- ✅ Port 8080 configured
- ✅ Gunicorn production server
- ✅ Auto-deployment enabled
- ✅ CORS enabled
- ✅ All 24 examples working

**Enjoy your deployed app!** 🚂
