# 🔧 Railway Port Fix

## Issue
Railway is starting gunicorn on port 5000 instead of using the PORT environment variable.

```
[INFO] Listening at: http://0.0.0.0:5000 (1)  ← Wrong port!
```

## Solution Applied

### 1. Created Start Script (`start.sh`)
```bash
#!/bin/bash
PORT=${PORT:-8080}
echo "Starting server on port $PORT"
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

This ensures the PORT variable is properly read and passed to gunicorn.

### 2. Updated Configuration Files
- ✅ **`Procfile`** → Uses `./start.sh`
- ✅ **`nixpacks.toml`** → Uses `bash start.sh`
- ✅ **`railway.json`** → Specifies start command
- ✅ **`start.sh`** → Made executable

## How to Fix on Railway

### Option A: Redeploy (Automatic)
```bash
git add .
git commit -m "Fix Railway port configuration"
git push origin main
```

Railway will auto-deploy with the new configuration.

### Option B: Manual Override in Railway Dashboard

1. Go to your Railway project
2. Click on your service
3. Go to **Settings**
4. Find **Start Command**
5. Set it to: `bash start.sh`
6. Click **Deploy** → **Redeploy**

### Option C: Set Environment Variable

1. Go to **Variables** tab in Railway
2. Add: `PORT = 8080` (or leave empty, Railway sets it automatically)
3. Redeploy

## Verify the Fix

After redeploying, check the logs. You should see:

```
Starting server on port 8080  ← Our script
[INFO] Listening at: http://0.0.0.0:8080  ← Correct port!
```

Or if Railway sets a different port:
```
Starting server on port 7543  ← Railway's PORT variable
[INFO] Listening at: http://0.0.0.0:7543  ← Matches!
```

## Why This Happened

Railway sets the `PORT` environment variable dynamically, but gunicorn wasn't reading it properly from the Procfile. The bash script ensures:

1. PORT is read from environment
2. Falls back to 8080 if not set
3. Explicitly passes it to gunicorn

## Next Steps

1. **Push the changes:**
   ```bash
   git add start.sh Procfile nixpacks.toml railway.json
   git commit -m "Fix Railway port configuration with start script"
   git push origin main
   ```

2. **Wait for Railway to redeploy** (1-2 minutes)

3. **Check logs** in Railway dashboard:
   - Should show: "Starting server on port XXXX"
   - Gunicorn should bind to same port

4. **Test your app** at the Railway URL

## Expected Logs After Fix

```
Starting Container
Starting server on port 8080
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8080 (1)  ← Correct!
[INFO] Using worker: sync
[INFO] Booting worker with pid: 2
[INFO] Booting worker with pid: 3
[INFO] Booting worker with pid: 4
```

## Troubleshooting

### Still shows port 5000?
1. Check if Railway picked up the new files
2. Try manual redeploy from Railway dashboard
3. Verify `start.sh` is executable (should be in git)

### Script not found?
1. Ensure `start.sh` is committed to git
2. Check file permissions: `chmod +x start.sh`
3. Try: `bash start.sh` instead of `./start.sh` in Procfile

### Port mismatch?
Railway sets PORT dynamically. Your app will bind to whatever Railway provides.

## Success Criteria

✅ Logs show "Starting server on port X"
✅ Gunicorn binds to same port X
✅ Railway URL is accessible
✅ All 24 examples work

---

**After pushing these changes, Railway should use the correct port!** 🚂
