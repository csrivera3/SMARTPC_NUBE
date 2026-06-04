import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.api.routers.auth import router as auth_router
from app.api.routers.employees import router as employees_router
from app.api.routers.users import router as users_router
from app.api.routers.invitations import router as invitations_router
from app.api.routers.agreements import router as agreements_router
from app.api.routers.meal_logs import router as meal_logs_router
from app.api.routers.qr import router as qr_router
from app.api.routers.reports import router as reports_router
from app.api.routers.companies import router as companies_router
from app.api.routers.restaurants import router as restaurants_router
from app.api.routes.entities import router as entities_router
from app.db.session import engine, SessionLocal
from app.db.base import Base

# Import models so metadata is populated before create_all
from app.models import User, Restaurant, Company, InvitationCode, Agreement, Employee, MealLog, Tenant, UserTenant, DeviceSession  # noqa: F401

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL.upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown event handler"""
    # Startup
    logger.info(f"Starting application in {settings.ENVIRONMENT} environment")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Initialize FastAPI app with enhanced documentation
app = FastAPI(
    title="MesaPass API",
    description="SaaS Multi-Tenant Platform - API Documentation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS with dynamic origins from settings
logger.info(f"Configuring CORS with origins: {settings.allowed_origins_list}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle pydantic validation errors with custom format"""
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])
        message = error["msg"]
        errors.append({
            "field": field,
            "message": message
        })
    
    logger.warning(f"Validation error for {request.url.path}: {errors}")
    
    return JSONResponse(
        status_code=422,
        content={
            "message": "Error de validación en los datos enviados",
            "status": 422,
            "error": True,
            "data": {
                "data": [],
                "errors": errors
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception for {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "message": "Error interno del servidor",
            "status": 500,
            "error": True
        }
    )


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Handle pydantic validation errors with custom format"""
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])
        message = error["msg"]
        errors.append({
            "field": field,
            "message": message
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "message": "Error de validación en los datos enviados",
            "status": 422,
            "error": True,
            "data": {
                "data": [],
                "errors": errors
            }
        }
    )


# Include routers - Multi-Tenant Routers
try:
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(employees_router, prefix="/api", tags=["entities"])
    app.include_router(users_router, prefix="/api", tags=["users"])
    app.include_router(invitations_router, prefix="/api", tags=["invitations"])
    app.include_router(agreements_router, prefix="/api", tags=["agreements"])
    app.include_router(meal_logs_router, prefix="/api", tags=["meal-logs"])
    app.include_router(qr_router, prefix="/api", tags=["qr"])
    app.include_router(reports_router, prefix="/api", tags=["reports"])
    app.include_router(companies_router, prefix="/api", tags=["companies"])
    app.include_router(restaurants_router, prefix="/api", tags=["restaurants"])
    
    # Legacy routers (kept for backward compatibility during migration)
    app.include_router(entities_router, prefix="/api", tags=["entities"])
    
    logger.info("All routers loaded successfully")
except Exception as e:
    logger.error(f"Error loading routers: {e}", exc_info=True)
    raise


# Health check endpoints
@app.get("/", tags=["health"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to MesaPass API - SaaS Multi-Tenant Platform",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "status": "online"
    }


@app.get("/health", tags=["health"])
async def health():
    """Basic health check - Always returns 200 if app is running"""
    return {
        "status": "ok",
        "service": "MesaPass API",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health/deep", tags=["health"])
async def health_deep():
    """Deep health check - Verifies database connectivity"""
    health_status = {
        "status": "ok",
        "service": "MesaPass API",
        "environment": settings.ENVIRONMENT,
        "database": "unknown"
    }
    
    try:
        # Test database connection
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
            health_status["database"] = "connected"
            logger.info("Database health check passed")
    except Exception as e:
        health_status["database"] = "disconnected"
        health_status["status"] = "degraded"
        logger.error(f"Database health check failed: {e}")
    
    return health_status


@app.get("/info", tags=["info"])
async def info():
    """API information endpoint"""
    return {
        "name": "MesaPass API",
        "version": "1.0.0",
        "description": "SaaS Multi-Tenant Platform for Restaurant Management",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "health": "/health",
            "health_deep": "/health/deep"
        }
    }

