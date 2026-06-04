# Deploy script for Railway - Windows PowerShell version
# Run from the project root directory: .\deploy-railway.ps1

Write-Host "======================================"
Write-Host "MesaPass Railway Deployment Script"
Write-Host "======================================"

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "ERROR: Git repository not found. Initialize with 'git init'" -ForegroundColor Red
    exit 1
}

# Show changes
Write-Host "Reviewing changes:" -ForegroundColor Yellow
git status

Write-Host "`nChanges to commit:" -ForegroundColor Yellow
git diff --name-only

# Confirm
$response = Read-Host "Are you sure you want to commit and push these changes? (y/n)"
if ($response -ne 'y' -and $response -ne 'Y') {
    Write-Host "Deployment cancelled."
    exit 1
}

# Add all changes
Write-Host "Adding changes..." -ForegroundColor Yellow
git add -A

# Commit
Write-Host "Committing changes..." -ForegroundColor Yellow
$commitMessage = @"
Fix: Remove hardcoded localhost references, require environment variables for Railway

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
silently connecting to non-existent localhost:5434.
"@

git commit -m $commitMessage

# Push
Write-Host "Pushing to remote..." -ForegroundColor Yellow
git push origin main

Write-Host "✓ Changes pushed successfully!" -ForegroundColor Green
Write-Host "⏳ Railway will automatically rebuild your deployment" -ForegroundColor Yellow
Write-Host "Monitor at: https://railway.app`n" -ForegroundColor Yellow

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Go to Railway Dashboard"
Write-Host "2. Click on your project > Settings > Variables"
Write-Host "3. Add DATABASE_URL from PostgreSQL plugin"
Write-Host "4. Add SECRET_KEY (generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))')"
Write-Host "5. Wait for rebuild to complete"
Write-Host "6. Test with: curl https://YOUR_RAILWAY_DOMAIN/health"
