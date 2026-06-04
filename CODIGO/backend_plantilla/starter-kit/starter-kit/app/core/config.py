import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Servidor
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    SKIP_DB_ON_STARTUP: bool = os.getenv("SKIP_DB_ON_STARTUP", "false").lower() == "true"
    
    # Base de datos - Requiere DATABASE_URL de entorno (ej: Railway PostgreSQL)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.DATABASE_URL:
            raise ValueError(
                "DATABASE_URL environment variable is required. "
                "Set it from your hosting provider (e.g., Railway PostgreSQL plugin)."
            )
    
    # Autenticación
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS - Requiere ALLOWED_ORIGINS de entorno para producción
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "")
    
    @property
    def allowed_origins_list(self) -> list:
        """Retorna lista de orígenes permitidos, o lista vacía si no configurado"""
        if not self.ALLOWED_ORIGINS:
            # En desarrollo sin CORS configurado, permitir localhost
            if self.ENVIRONMENT == "development":
                return [
                    "http://localhost:3000",
                    "http://localhost:3001", 
                    "http://127.0.0.1:3000"
                ]
            else:
                # En producción, CORS es requerido
                raise ValueError(
                    "ALLOWED_ORIGINS environment variable is required for production. "
                    "Set it to your frontend domain (e.g., https://yourdomain.com)"
                )
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
