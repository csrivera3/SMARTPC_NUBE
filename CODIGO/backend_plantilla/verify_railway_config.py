#!/usr/bin/env python3
"""
Railway Deployment Verification Script
=====================================

This script verifies that your application is properly configured for Railway deployment.

Usage:
    python verify_railway_config.py

It checks:
    1. All required environment variables are set
    2. DATABASE_URL format is correct (if set)
    3. Application can import all modules
    4. Database connection can be established (if DATABASE_URL is set)
    5. FastAPI app initializes without errors
"""

import sys
import os
from pathlib import Path

# Add the starter-kit directory to Python path
starter_kit_path = Path(__file__).parent / "starter-kit" / "starter-kit"
sys.path.insert(0, str(starter_kit_path))

def check_environment_variables():
    """Check if required environment variables are set"""
    print("\n1️⃣  CHECKING ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    required_vars = {
        "ENVIRONMENT": "production or development",
        "SECRET_KEY": "for JWT token signing (can be dummy in dev)",
        "DEBUG": "true or false",
    }
    
    optional_vars = {
        "DATABASE_URL": "PostgreSQL connection string (auto-set by Railway)",
        "ALLOWED_ORIGINS": "comma-separated CORS origins",
        "LOG_LEVEL": "info, debug, warning, error",
    }
    
    print("\n✓ REQUIRED VARIABLES:")
    for var, desc in required_vars.items():
        value = os.getenv(var, "NOT SET")
        status = "✓" if value != "NOT SET" else "✗"
        print(f"  {status} {var:20} = {value[:50] if value != 'NOT SET' else 'NOT SET'}")
    
    print("\n✓ OPTIONAL VARIABLES:")
    for var, desc in optional_vars.items():
        value = os.getenv(var, "NOT SET")
        if value != "NOT SET":
            print(f"  ✓ {var:20} = {value[:50]}")
        else:
            print(f"  ℹ {var:20} = NOT SET (using defaults)")
    
    database_url = os.getenv("DATABASE_URL")
    print("\n📊 DATABASE_URL STATUS:")
    if database_url:
        print(f"  ✓ DATABASE_URL is configured")
        # Don't print the actual URL for security
        print(f"  ✓ Format appears to be: {database_url.split('://')[0]}://...")
    else:
        print(f"  ⚠️  DATABASE_URL not configured")
        print(f"  → App will start but database operations may fail")
        print(f"  → Configure in Railway Dashboard → Variables")


def check_imports():
    """Check if all required modules can be imported"""
    print("\n2️⃣  CHECKING PYTHON IMPORTS")
    print("=" * 60)
    
    critical_imports = [
        "fastapi",
        "sqlalchemy",
        "pydantic",
        "qrcode",
        "PIL",
        "requests",
        "httpx",
        "email_validator",
        "python_multipart",
    ]
    
    print("\n✓ CRITICAL DEPENDENCIES:")
    for module in critical_imports:
        try:
            __import__(module)
            print(f"  ✓ {module:20} - OK")
        except ImportError as e:
            print(f"  ✗ {module:20} - FAILED: {e}")
            return False
    
    return True


def check_config():
    """Check if app configuration loads"""
    print("\n3️⃣  CHECKING APPLICATION CONFIG")
    print("=" * 60)
    
    try:
        from app.core.config import settings
        print(f"\n✓ Configuration loaded successfully")
        print(f"  - ENVIRONMENT: {settings.ENVIRONMENT}")
        print(f"  - DEBUG: {settings.DEBUG}")
        print(f"  - LOG_LEVEL: {settings.LOG_LEVEL}")
        print(f"  - DATABASE_URL: {'configured' if settings.DATABASE_URL else 'NOT configured'}")
        print(f"  - ALLOWED_ORIGINS: {len(settings.allowed_origins_list)} origin(s)")
        return True
    except Exception as e:
        print(f"✗ Configuration failed: {e}")
        return False


def check_database_connection():
    """Check if database connection works"""
    print("\n4️⃣  CHECKING DATABASE CONNECTION")
    print("=" * 60)
    
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("\n⚠️  DATABASE_URL not set - skipping database check")
        print("  This is OK for initial Railway setup")
        print("  Configure DATABASE_URL in Railway Dashboard")
        return True
    
    try:
        from sqlalchemy import create_engine, text
        from app.core.config import settings
        
        print(f"\n⚠️  Attempting to connect to database...")
        print(f"  (This may fail if Railway database is not running)")
        
        engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"client_encoding": "utf8", "connect_timeout": 5},
            pool_pre_ping=True,
        )
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"✓ Database connection successful")
            return True
            
    except Exception as e:
        print(f"✗ Database connection failed")
        print(f"  Error: {str(e)[:100]}")
        print(f"\n  This is expected if:")
        print(f"    1. DATABASE_URL is not configured in Railway")
        print(f"    2. PostgreSQL database is not running")
        print(f"    3. Connection credentials are wrong")
        return False


def check_fastapi_app():
    """Check if FastAPI app can initialize"""
    print("\n5️⃣  CHECKING FASTAPI APPLICATION")
    print("=" * 60)
    
    try:
        from app.main import app
        print(f"\n✓ FastAPI application initialized successfully")
        print(f"  - Title: {app.title}")
        print(f"  - Routes: {len(app.routes)}")
        print(f"  - Routers: {len([r for r in app.routes if hasattr(r, 'path')])}")
        
        # Try health check endpoint
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.get("/health")
        print(f"\n  - /health endpoint: {response.status_code}")
        print(f"    Response: {response.json()}")
        
        return True
    except Exception as e:
        print(f"✗ FastAPI app initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all checks"""
    print("\n" + "=" * 60)
    print("🚀 RAILWAY DEPLOYMENT VERIFICATION SCRIPT")
    print("=" * 60)
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("Python Imports", check_imports),
        ("App Configuration", check_config),
        ("Database Connection", check_database_connection),
        ("FastAPI Application", check_fastapi_app),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} check failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "⚠ WARNING/FAIL"
        print(f"  {status:15} - {name}")
    
    print("\n" + "=" * 60)
    
    # Overall status
    critical_checks = results[:4]  # All except DB connection
    all_critical_pass = all(result for _, result in critical_checks)
    
    if all_critical_pass:
        print("\n✅ READY FOR RAILWAY DEPLOYMENT!")
        print("\nNext steps:")
        print("  1. Commit and push your code")
        print("  2. Railway will automatically deploy")
        print("  3. Configure DATABASE_URL in Railway Dashboard")
        print("  4. Verify deployment with: /health and /health/deep endpoints")
        return 0
    else:
        print("\n⚠️  ISSUES FOUND - Please fix before deploying")
        print("\nCommon fixes:")
        print("  - Install missing dependencies: pip install -r requirements.txt")
        print("  - Set ENVIRONMENT variable: export ENVIRONMENT=production")
        print("  - Set DEBUG variable: export DEBUG=false")
        return 1


if __name__ == "__main__":
    sys.exit(main())
