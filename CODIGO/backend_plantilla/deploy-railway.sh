#!/bin/bash
# Deploy script for Railway - Commit and push changes

set -e

echo "======================================"
echo "MesaPass Railway Deployment Script"
echo "======================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${RED}✗ Git repository not found. Initialize with 'git init'${NC}"
    exit 1
fi

# Show changes
echo -e "${YELLOW}Reviewing changes:${NC}"
git status

echo -e "${YELLOW}\nChanges to commit:${NC}"
git diff --name-only

# Confirm
read -p "Are you sure you want to commit and push these changes? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

# Add all changes
echo -e "${YELLOW}Adding changes...${NC}"
git add -A

# Commit
echo -e "${YELLOW}Committing changes...${NC}"
git commit -m "Fix: Remove hardcoded localhost references, require environment variables for Railway

Changed Files:
- app/core/config.py: DATABASE_URL now required, CORS uses env or development defaults
- setup_db.py: Parse DATABASE_URL from environment instead of hardcoded credentials
- run_server.py: Use environment variables for host/port/workers
- migrations/env.py: Validate DATABASE_URL before running migrations
- Dockerfile: Fix health check to use proper host
- .env.example: Updated with current configuration template

This fixes 'Application failed to respond' error in Railway deployment by:
✓ Removing all hardcoded localhost references
✓ Requiring explicit DATABASE_URL configuration
✓ Making CORS configuration flexible for production
✓ Supporting Railway PostgreSQL managed database
✓ Improving error messages for missing configuration

Impact: App now fails fast if DATABASE_URL is missing (clear error) instead of
silently connecting to non-existent localhost:5434."

# Push
echo -e "${YELLOW}Pushing to remote...${NC}"
git push origin main

echo -e "${GREEN}✓ Changes pushed successfully!${NC}"
echo -e "${YELLOW}⏳ Railway will automatically rebuild your deployment${NC}"
echo -e "${YELLOW}Monitor at: https://railway.app${NC}"
echo -e "\n${YELLOW}Next Steps:${NC}"
echo "1. Go to Railway Dashboard"
echo "2. Click on your project > Settings > Variables"
echo "3. Add DATABASE_URL from PostgreSQL plugin"
echo "4. Add SECRET_KEY (generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\")"
echo "5. Wait for rebuild to complete"
echo "6. Test with: curl https://YOUR_RAILWAY_DOMAIN/health"
