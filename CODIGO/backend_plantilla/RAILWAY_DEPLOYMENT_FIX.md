# Railway Deployment Fix - Eliminar Hardcodes de Localhost

## 🎯 Problema Identificado

**Error en Railway:** "Application failed to respond"

**Causa Raíz:** El código contenía 15 referencias hardcodeadas a `localhost:5434` que impedía que Railway conectara la base de datos PostgreSQL.

## ✅ Cambios Implementados

### 1. **app/core/config.py** - Base de Datos Requerida (CRÍTICO)
```python
# ANTES (Línea 18):
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:1324@localhost:5434/mesa_db"  # ❌ HARDCODED
)

# DESPUÉS:
DATABASE_URL: str = os.getenv("DATABASE_URL", "")

def __init__(self, **data):
    super().__init__(**data)
    if not self.DATABASE_URL:
        raise ValueError(
            "DATABASE_URL environment variable is required. "
            "Set it from your hosting provider (e.g., Railway PostgreSQL plugin)."
        )
```

**Impacto:** App falla si DATABASE_URL no está configurado (mejor que usar localhost silenciosamente).

### 2. **app/core/config.py** - CORS Inteligente (ALTO)
```python
# ANTES (Línea 30):
ALLOWED_ORIGINS: str = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"  # ❌ HARDCODED
)

# DESPUÉS:
ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "")

@property
def allowed_origins_list(self) -> list:
    if not self.ALLOWED_ORIGINS:
        if self.ENVIRONMENT == "development":
            # Localhost en desarrollo
            return ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"]
        else:
            # Producción requiere dominio
            raise ValueError("ALLOWED_ORIGINS required for production")
    return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
```

**Impacto:** Desarrollo usa localhost automáticamente, producción requiere configuración.

### 3. **setup_db.py** - Credenciales de Entorno (CRÍTICO)
```python
# ANTES: hardcoded host="localhost", port=5434, user="postgres", password="1324"
# DESPUÉS: Parse DATABASE_URL y obtiene credenciales del entorno
```

**Impacto:** Script ahora funciona con Railway PostgreSQL o cualquier base de datos remota.

### 4. **run_server.py** - Sin Rutas Hardcodeadas (ALTO)
```python
# ANTES: os.chdir(r'c:\Users\Lenovo\Downloads\...')  # ❌ Ruta absoluta local
# DESPUÉS: Uso de variables de entorno:
host = os.getenv("HOST", "127.0.0.1")
port = os.getenv("PORT", "8000")
reload_mode = os.getenv("RELOAD", "true").lower() == "true"
workers = int(os.getenv("WORKERS", "1"))
```

**Impacto:** Script funciona en cualquier máquina/servidor.

### 5. **migrations/env.py** - DATABASE_URL Validado (CRÍTICO)
```python
# Ahora valida que DATABASE_URL esté configurado antes de ejecutar migraciones
# Antes usaba settings.DATABASE_URL que podría ser localhost
```

**Impacto:** Las migraciones fallan claramente si DATABASE_URL falta, en lugar de conectar a localhost.

### 6. **Dockerfile** - Health Check Reparado (MEDIO)
```dockerfile
# ANTES: curl -f http://localhost:${PORT:-8000}/health
# DESPUÉS: curl -f http://127.0.0.1:${PORT:-8000}/health
```

**Impacto:** Health check puede ser alcanzable dentro del contenedor.

## 🚀 Pasos de Despliegue

### Paso 1: Confirmar los Cambios Localmente

```bash
# Ir a la carpeta del proyecto
cd c:\Users\Lenovo\OneDrive\Escritorio\SMARTPC_NUBE\CODIGO\backend_plantilla\starter-kit\starter-kit

# Crear archivo .env.local para pruebas
# (Usa DATABASE_URL de tu servidor local o remoto)
cat > .env.local << 'EOF'
ENVIRONMENT=development
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/mesa_db
SECRET_KEY=your-test-secret-key-12345
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
DEBUG=true
LOG_LEVEL=debug
EOF

# Probar la aplicación
python run_server.py
# Debe iniciar sin error de hardcoded localhost
```

### Paso 2: Git Commit

```bash
# Navegar a la raíz del proyecto
cd c:\Users\Lenovo\OneDrive\Escritorio\SMARTPC_NUBE\CODIGO\backend_plantilla

# Ver cambios
git status

# Agregar cambios
git add -A

# Commit
git commit -m "Fix: Remove hardcoded localhost references, require environment variables for Railway deployment

- app/core/config.py: DATABASE_URL now required, CORS uses env or development defaults
- setup_db.py: Parse DATABASE_URL from environment instead of hardcoded credentials
- run_server.py: Use environment variables for host/port/workers
- migrations/env.py: Validate DATABASE_URL before running migrations
- Dockerfile: Fix health check to use proper host

This fixes 'Application failed to respond' error in Railway deployment."

# Push a GitHub/GitLab
git push origin main
```

### Paso 3: Configurar Railway Dashboard

**EN RAILWAY.APP:**

1. **Ir a tu Proyecto MesaPass**
2. **Click en tu Railway Environment (ej: Production)**
3. **Click en Settings/Variables**
4. **Agregar Estas Variables:**

```
DATABASE_URL = [copiar de PostgreSQL plugin connection string]
SECRET_KEY = [generar algo seguro]
ENVIRONMENT = production
DEBUG = false
LOG_LEVEL = info
ALLOWED_ORIGINS = https://yourdomain.com,https://www.yourdomain.com
SKIP_DB_ON_STARTUP = false
```

### Paso 4: Obtener DATABASE_URL de Railway

**EN RAILWAY.APP:**

1. **Click en el Plugin PostgreSQL** (tu base de datos)
2. **Click en "Connect"**
3. **Copiar la URL que dice "Postgres Connection URL"**
4. **Pegar en la variable DATABASE_URL del environment**

Ejemplo:
```
postgresql://postgres:AbCdEfG@containers-us-west-XXX.railway.app:5432/railway
```

### Paso 5: Generar SECRET_KEY Segura

```bash
# En PowerShell:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copiar el resultado y pegarlo en Railway como SECRET_KEY
```

### Paso 6: Trigger Rebuild en Railway

1. **Ir a Deployments en Railway**
2. **Click en el último deployment**
3. **Click "Redeploy"** O
4. **Hacer push a GitHub** (si está conectado)

Railway automaticamente rebuildeará el contenedor con las nuevas variables.

## 🧪 Verificación Post-Despliegue

```bash
# Reemplazar YOUR_RAILWAY_DOMAIN con el actual (ej: mesapass.railway.app)
DOMAIN="YOUR_RAILWAY_DOMAIN"

# Test 1: Health Check (no requiere DB)
curl https://$DOMAIN/health
# Esperado: {"status":"ok","service":"MesaPass API","environment":"production"}

# Test 2: Info Endpoint (no requiere DB)
curl https://$DOMAIN/info
# Esperado: {"name":"MesaPass API",...}

# Test 3: Root Endpoint (no requiere DB)
curl https://$DOMAIN/
# Esperado: {"message":"Welcome to MesaPass API",...}

# Test 4: Deep Health (requiere DB - verifica conexión)
curl https://$DOMAIN/health/deep
# Esperado: {"status":"ok","database":"connected",...}
```

## ❌ Si Falla Aún

### Error: "VALUE_ERROR: DATABASE_URL environment variable is required"

**Solución:** La variable DATABASE_URL no está configurada en Railway Dashboard.
- Ir a Railway > Variables > agregar DATABASE_URL
- Debe tener formato: `postgresql://user:pass@host:port/database`

### Error: "Application failed to respond"

1. **Ver logs:** En Railway Dashboard > Deployments > View Logs
2. **Buscar:** "DATABASE_URL environment variable is required"
3. **Si no aparece:** Significa que DATABASE_URL está configurado correctamente
4. **Revisar:** Que SECRET_KEY también esté configurado

### Error: "ALLOWED_ORIGINS environment variable is required for production"

**Solución:** Configurar ALLOWED_ORIGINS en Railway con tu dominio frontend:
```
ALLOWED_ORIGINS=https://yourdomain.com
```

## 📋 Checklist Completo

- [ ] Cambios de código implementados (app/core/config.py, setup_db.py, etc.)
- [ ] Git commit y push realizados
- [ ] Railway DATABASE_URL configurada ✅
- [ ] Railway SECRET_KEY configurada ✅
- [ ] Railway ENVIRONMENT=production configurada ✅
- [ ] Railway DEBUG=false configurada ✅
- [ ] Railway ALLOWED_ORIGINS configurada con tu dominio ✅
- [ ] Rebuild triggered en Railway ✅
- [ ] Health endpoints responden (GET /health) ✅
- [ ] Deep health check pasa (GET /health/deep) ✅

## 🎉 ¡Listo!

Tu aplicación ahora:
- ✅ No usa hardcoded localhost
- ✅ Requiere configuración explícita de DATABASE_URL
- ✅ Funciona con Railway PostgreSQL
- ✅ Es prod-ready sin dependencias de máquina local
- ✅ Fallapidamente si faltan variables (mejor que conectar a servidor equivocado)
