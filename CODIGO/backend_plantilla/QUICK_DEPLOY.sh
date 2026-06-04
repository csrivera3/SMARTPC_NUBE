#!/usr/bin/env bash
# 🚀 RAILWAY DEPLOYMENT - QUICK START COMMANDS
# Copy and paste these commands in order to deploy to Railway

echo "================================================"
echo "🚀 RAILWAY DEPLOYMENT - QUICK START"
echo "================================================"
echo ""

# Step 1: Check git status
echo "📌 Step 1: Check git status"
echo "---"
echo "git status"
echo ""

# Step 2: Stage all changes
echo "📌 Step 2: Stage changes"
echo "---"
echo "git add ."
echo "git status  # Verify all files are staged"
echo ""

# Step 3: Commit
echo "📌 Step 3: Commit changes"
echo "---"
echo 'git commit -m "🚀 feat(railway): Production-ready FastAPI deployment

- Add database tolerance during startup (SKIP_DB_ON_STARTUP)
- Implement graceful error handling for DB initialization
- Configure SQLAlchemy connection pooling with health checks
- Add railway-migrate.sh for separate schema migrations
- Update .env.railway template with production config
- Add comprehensive logging for debugging in production
- Fix: Handle Railway environment variables correctly
- Fix: Prevent localhost hardcoding in production"'
echo ""

# Step 4: Push to main
echo "📌 Step 4: Push to Railway (triggers automatic deployment)"
echo "---"
echo "git push origin main"
echo ""
echo "⏳ Wait for Railway to build and deploy (check Railway Dashboard)"
echo ""

# Step 5: Configure variables
echo "📌 Step 5: Railway Dashboard Configuration"
echo "---"
echo "Go to: https://railway.app"
echo "Project → Environment → Variables"
echo ""
echo "Add these variables:"
echo "  ENVIRONMENT=production"
echo "  DEBUG=false"
echo "  LOG_LEVEL=info"
echo "  SKIP_DB_ON_STARTUP=false"
echo "  DATABASE_URL=<copy from PostgreSQL plugin>"
echo "  SECRET_KEY=<run: python -c \"import secrets; print(secrets.token_urlsafe(32))\">"
echo "  ALLOWED_ORIGINS=https://your-railway-domain.up.railway.app"
echo "  APP_VERSION=1.0.0"
echo "  APP_NAME=MesaPass API"
echo ""

# Step 6: Run migrations
echo "📌 Step 6: Execute database migrations"
echo "---"
echo "Option A (with Railway CLI):"
echo "  railway run bash railway-migrate.sh"
echo ""
echo "Option B (from local machine):"
echo "  export DATABASE_URL='<PostgreSQL connection string from Railway>'"
echo "  cd starter-kit"
echo "  alembic upgrade head"
echo ""

# Step 7: Verify
echo "📌 Step 7: Verify deployment"
echo "---"
echo "curl https://your-railway-domain.up.railway.app/health"
echo "curl https://your-railway-domain.up.railway.app/info"
echo ""

# Step 8: Check logs
echo "📌 Step 8: Monitor logs"
echo "---"
echo "railway logs  # If CLI is installed"
echo ""
echo "OR check in Railway Dashboard → Deployments → Logs"
echo ""

echo "================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================================"
echo ""
echo "📚 Documentation:"
echo "  - RAILWAY_PRODUCTION_DEPLOY.md - Full step-by-step guide"
echo "  - RAILWAY_DATABASE_FIX.md - Problem analysis and solution"
echo "  - .env.railway - Environment template"
echo ""
echo "🔗 Resources:"
echo "  - Railway Dashboard: https://railway.app"
echo "  - API Docs: https://your-railway-domain.up.railway.app/docs"
echo "  - Health Check: https://your-railway-domain.up.railway.app/health"
echo ""
