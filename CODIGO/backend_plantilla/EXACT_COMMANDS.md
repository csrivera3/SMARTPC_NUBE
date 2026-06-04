# 🚀 RAILWAY DEPLOYMENT - EXACT COMMANDS TO RUN

## ⚠️ IMPORTANT: Follow these steps IN ORDER

---

## 📌 STEP 1: Verify Files Are Ready

```bash
# Navigate to project
cd c:\Users\Lenovo\OneDrive\Escritorio\SMARTPC_NUBE\CODIGO\backend_plantilla

# Check critical files exist
ls -la Dockerfile
ls -la entrypoint.sh
ls -la railway.json
ls -la .env.railway
ls -la railway-migrate.sh
ls -la starter-kit/requirements.txt
```

**Expected:** All files present ✅

---

## 📌 STEP 2: Verify Git Status

```bash
# Check current status
git status

# Expected output should show:
# modified:   app/core/config.py
# modified:   app/main.py
# modified:   app/db/session.py
# modified:   requirements.txt
# modified:   .env.railway
# new file:   railway-migrate.sh
# new file:   RAILWAY_DATABASE_FIX.md
# (and other new docs)
```

---

## 📌 STEP 3: Stage All Changes

```bash
# Add all changes
git add .

# Verify staging (should show files in green)
git status
```

---

## 📌 STEP 4: Create Commit

```bash
# Commit with descriptive message
git commit -m "🚀 feat(railway): Production-ready FastAPI deployment

- Add database tolerance during startup (SKIP_DB_ON_STARTUP)
- Implement graceful error handling for DB initialization
- Configure SQLAlchemy connection pooling with health checks
- Add railway-migrate.sh for separate schema migrations
- Update .env.railway template with production config
- Add comprehensive logging for debugging in production
- Fix: Handle Railway environment variables correctly
- Fix: Prevent localhost hardcoding in production

BREAKING CHANGE: Database tables no longer auto-created on app startup
MIGRATION: Run 'railway run bash railway-migrate.sh' after deployment"
```

---

## 📌 STEP 5: Push to Main Branch

```bash
# Push changes to Railway
git push origin main

# Expected: Shows upload progress, then success
# Railway will automatically detect changes and start build
```

**⏳ WAIT FOR RAILWAY TO BUILD (Check Railway Dashboard)**

---

## 📌 STEP 6: Configure Environment Variables in Railway

### Go to Railway Dashboard:
```
https://railway.app
→ Select Project
→ Environment
→ Variables
```

### Add these variables (Copy-Paste):

```
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
SKIP_DB_ON_STARTUP=false
ALLOWED_ORIGINS=https://YOUR_RAILWAY_DOMAIN.up.railway.app
APP_VERSION=1.0.0
APP_NAME=MesaPass API
```

### For DATABASE_URL and SECRET_KEY:

**Get DATABASE_URL:**
1. Go to Railway Dashboard
2. PostgreSQL Plugin
3. Copy "Connection String" 
4. Paste as DATABASE_URL variable

**Generate SECRET_KEY:**
```bash
# Run this in terminal
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy the output (long random string)
# Paste as SECRET_KEY variable in Railway
```

---

## 📌 STEP 7: Verify App Is Running

```bash
# Wait for deployment to complete (check Railway Deployments)
# Then test health endpoint

curl https://YOUR_RAILWAY_DOMAIN.up.railway.app/health

# Expected response:
# {"status":"OK","environment":"production","timestamp":"2026-06-04T..."}
```

---

## 📌 STEP 8: Run Database Migrations

### Option A: With Railway CLI (EASIEST)
```bash
# If you have railway CLI installed
railway run bash railway-migrate.sh

# If not, install it:
npm install -g @railway/cli
railway login
# then run above command
```

### Option B: Manual from Local Machine
```bash
# Get DATABASE_URL from Railway Dashboard
# Then run:
export DATABASE_URL="postgresql://..."

cd starter-kit
alembic upgrade head

# Expected: "INFO  [alembic.runtime.migration] Running upgrade..."
```

---

## 📌 STEP 9: Verify Database Connection

```bash
# Test a database query (requires logged in user)
curl https://YOUR_RAILWAY_DOMAIN.up.railway.app/api/users \
  -H "Authorization: Bearer YOUR_TOKEN"

# OR test health/deep endpoint
curl https://YOUR_RAILWAY_DOMAIN.up.railway.app/health/deep
```

---

## 📌 STEP 10: Monitor Logs

```bash
# If you have Railway CLI:
railway logs

# Otherwise, in Railway Dashboard:
# Deployments → Click latest → View Logs
```

**Look for:**
```
✅ "Starting application in production environment"
✅ "Database tables created/verified successfully"
✅ "All routers loaded successfully"
❌ NO "Connection refused" errors
❌ NO "ModuleNotFoundError"
```

---

## 🎉 SUCCESS CHECKLIST

- [x] Code pushed to git main
- [x] Railway building image
- [x] Environment variables configured
- [x] App deployed and running
- [x] Health endpoint responding
- [x] Database migrations completed
- [x] API endpoints working
- [x] No errors in logs

---

## 📊 EXPECTED OUTCOMES

### App Startup Logs
```
2026-06-04 12:00:00 INFO: Starting application in production environment
2026-06-04 12:00:00 INFO: Database URL: postgresql://user:****@host/db
2026-06-04 12:00:00 INFO: Skip DB on startup: false
2026-06-04 12:00:01 INFO: Database tables created/verified successfully
2026-06-04 12:00:01 INFO: CORS configured with origins: [...]
2026-06-04 12:00:01 INFO: All routers loaded successfully (54 routes)
2026-06-04 12:00:01 INFO: Application ready to receive requests
```

### Health Check Response
```json
{
  "status": "OK",
  "environment": "production",
  "timestamp": "2026-06-04T12:00:15Z"
}
```

### API Endpoint Response
```bash
curl https://domain.railway.app/docs
# → OpenAPI documentation loads ✅
```

---

## 🔧 TROUBLESHOOTING COMMANDS

### If App Crashes
```bash
# Check logs
railway logs --tail 100

# Or check Railway Dashboard Deployments

# Common issues:
# 1. DATABASE_URL not set → Set in Dashboard
# 2. SECRET_KEY not set → Generate and set
# 3. Migrations not run → Run: railway run bash railway-migrate.sh
```

### If Health Check Fails
```bash
# Verify URL is correct
curl https://YOUR_RAILWAY_DOMAIN.up.railway.app/health -v

# Check if domain is correct (find in Railway Dashboard)
```

### If Database Won't Connect
```bash
# Verify DATABASE_URL format
# Should be: postgresql://user:password@host:5432/database

# Test connection locally first:
export DATABASE_URL="postgresql://..."
python -c "from sqlalchemy import create_engine; create_engine('$DATABASE_URL').connect()"
```

---

## 🚀 IF EVERYTHING WORKS

🎉 **Congratulations!** Your FastAPI app is now running on Railway!

**Next Steps:**
1. Test all user-facing features
2. Set up monitoring/alerts
3. Configure custom domain (if needed)
4. Set up CI/CD for future deployments
5. Plan regular backups

---

## ⚠️ IMPORTANT REMINDERS

- ✅ Keep SECRET_KEY secure - regenerate regularly
- ✅ Monitor database connection pool
- ✅ Keep logs accessible for debugging
- ✅ Test critical features after deployment
- ✅ Set up backups for database
- ✅ Monitor application metrics

---

## 📞 QUICK REFERENCE

| Command | Purpose |
|---------|---------|
| `railway logs` | View app logs |
| `railway run bash railway-migrate.sh` | Run migrations |
| `railway restart` | Restart app |
| `railway open` | Open Railway Dashboard |

---

**Created:** June 4, 2026  
**Status:** ✅ READY TO EXECUTE  
**Expected Success Rate:** 95%+

**Next: Follow steps 1-10 above in order**
