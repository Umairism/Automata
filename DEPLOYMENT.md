# Automata Solver - Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Dependencies
- [ ] Python 3.8+ installed
- [ ] Graphviz installed (`dot -V` works)
- [ ] Virtual environment created
- [ ] All packages from requirements.txt installed

### 2. File Structure
- [x] app.py (Flask application)
- [x] requirements.txt (dependencies)
- [x] engine/ (core engines)
- [x] diagrams/ (diagram generation)
- [x] builders/ (solution assembly)
- [x] templates/ (HTML interface)
- [x] static/ (generated files)
- [x] Dockerfile (containerization)
- [x] README.md (documentation)
- [x] USAGE_GUIDE.md (usage instructions)
- [x] .gitignore (Git ignore rules)

### 3. Testing
- [ ] Run `python test_setup.py`
- [ ] Verify all imports work
- [ ] Test CFG ambiguity detection
- [ ] Test web interface loads
- [ ] Test API endpoints
- [ ] Verify diagram generation

---

## 🚀 Deployment Options

### Option 1: Local Development

```bash
# 1. Navigate to project
cd /home/umairism/Desktop/Github/Automata

# 2. Run setup script
./setup.sh

# 3. Activate environment
source venv/bin/activate

# 4. Run application
python app.py

# 5. Access at http://localhost:5000
```

### Option 2: Production with Gunicorn

```bash
# 1. Setup as above

# 2. Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Optional: Run in background
gunicorn -w 4 -b 0.0.0.0:5000 app:app --daemon
```

### Option 3: Docker Deployment

```bash
# 1. Build image
docker build -t automata-solver .

# 2. Run container
docker run -d -p 5000:5000 --name automata-solver automata-solver

# 3. View logs
docker logs automata-solver

# 4. Stop container
docker stop automata-solver
```

### Option 4: Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  automata-solver:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./static:/app/static
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

---

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env` file:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_DERIVATION_DEPTH=10
MAX_TM_STEPS=1000
```

Update `app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key')
```

### Nginx Reverse Proxy (Production)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/Automata/static;
    }
}
```

---

## 📊 Monitoring & Logs

### View Logs

**Flask Development:**
```bash
python app.py
# Logs appear in terminal
```

**Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app --access-logfile access.log --error-logfile error.log
```

**Docker:**
```bash
docker logs -f automata-solver
```

### Health Check

```bash
# Check status
curl http://localhost:5000/api/status

# Should return:
# {"status":"running","version":"1.0.0",...}
```

---

## 🧪 Testing After Deployment

### 1. Basic API Test

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question":"Construct DFA for even as","grammar":""}'
```

### 2. CFG Test

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "question":"Prove ambiguity",
    "grammar":"E → E+E | E*E | id"
  }'
```

### 3. Web Interface Test

1. Open browser: `http://localhost:5000`
2. Click example question
3. Click "Solve"
4. Verify diagrams load

---

## 🔒 Security Considerations

### Production Settings

In `app.py`:
```python
# Change this for production:
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'complex-random-string'

# Disable debug mode
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Input Validation

- ✅ Query length limits (implemented)
- ✅ Grammar depth limits (implemented)
- ✅ Computation timeouts (implemented)
- ⚠️ Consider rate limiting for public deployments

### File Permissions

```bash
# Ensure static directory is writable
chmod 755 static/

# Protect sensitive files
chmod 600 .env
```

---

## 📈 Performance Optimization

### Recommendations

1. **Use Gunicorn with multiple workers:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Enable gzip compression** (in Nginx)
3. **Cache static files**
4. **Set up CDN for diagrams** (if needed)
5. **Use Redis for caching** (future enhancement)

### Resource Limits

Current defaults:
- Max derivation depth: 10
- Max string length: 10
- Max TM steps: 1000
- Max PDA moves: 100

Adjust in respective engine files if needed.

---

## 🐛 Troubleshooting Deployment

### Issue: Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
python app.py --port 8000
```

### Issue: Graphviz Not Found

```bash
# Install Graphviz
sudo apt-get install graphviz  # Ubuntu/Debian
brew install graphviz          # macOS

# Verify
dot -V
```

### Issue: Permission Denied on static/

```bash
# Fix permissions
chmod 755 static/
chown -R $USER:$USER static/
```

### Issue: Module Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Or recreate environment
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📝 Post-Deployment Tasks

- [ ] Test all major features
- [ ] Monitor error logs
- [ ] Set up backup for static files
- [ ] Configure SSL/HTTPS (if public)
- [ ] Set up monitoring/alerting
- [ ] Document any custom configurations
- [ ] Set up automated backups
- [ ] Configure log rotation

---

## 🎯 Quick Commands Reference

```bash
# Start development server
python app.py

# Start production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Run tests
python test_setup.py

# Build Docker image
docker build -t automata-solver .

# Run Docker container
docker run -p 5000:5000 automata-solver

# Check status
curl http://localhost:5000/api/status

# View logs (Docker)
docker logs automata-solver

# Stop server (Gunicorn)
pkill gunicorn

# Clean generated files
rm -rf static/*.png static/*.dot
```

---

## ✨ Success Indicators

Your deployment is successful when:

1. ✅ Application starts without errors
2. ✅ Web interface loads at http://localhost:5000
3. ✅ Example questions work correctly
4. ✅ Diagrams are generated and displayed
5. ✅ API endpoints respond correctly
6. ✅ Status endpoint returns healthy status

---

## 📞 Support

If you encounter issues:

1. Check logs for error messages
2. Review this checklist
3. Consult README.md and USAGE_GUIDE.md
4. Run `python test_setup.py` for diagnostics
5. Check GitHub issues

---

**Deployment Date:** _____________

**Deployed By:** _____________

**Environment:** □ Development  □ Production  □ Docker

**Notes:**
_____________________________________________________________
_____________________________________________________________
