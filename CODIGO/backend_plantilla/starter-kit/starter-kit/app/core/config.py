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
    
    # Base de datos - Soporta DATABASE_URL (Railway) o credenciales individuales
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:1324@localhost:5434/mesa_db"
    )
    
    # Autenticación
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS - Soporta múltiples orígenes separados por coma
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"
    )
    
    @property
    def allowed_origins_list(self) -> list:
        """Retorna lista de orígenes permitidos"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
