# 🚀 RAILWAY SETUP GUIDE - MesaPass Backend

## 📋 PROBLEMA ANTERIOR

El error de conexión a BD ocurría porque:
- La aplicación intentaba conectarse a `localhost:5434` durante el startup
- Railway no tiene una BD corriendo en localhost
- La variable `DATABASE_URL` no estaba configurada en Railway

## ✅ SOLUCIÓN IMPLEMENTADA

### 1. Código Mejorado
La aplicación ahora:
- ✅ No falla si la BD no está disponible en startup
- ✅ Proporciona feedback claro sobre el estado de la BD
- ✅ Usa `NullPool` en Railway (mejor para serverless)
- ✅ Usa pool normal en desarrollo

### 2. Health Checks Mejorados
- `/health` - Devuelve estado de la app y BD
- `/health/deep` - Test completo de conectividad

---

## 🔧 CONFIGURACIÓN EN RAILWAY

### PASO 1: Crear Base de Datos PostgreSQL

1. En Railway Dashboard → Project
2. **+ Create** → **Database** → **PostgreSQL**
3. Esperar a que se cree (2-3 minutos)

### PASO 2: Conectar Base de Datos a la App

1. Ir a tu servicio `smartpcnube-production`
2. **Variables** → Verifica que exista:
   ```
   DATABASE_URL = postgresql://user:password@host:port/dbname
   ```
   
3. Si no existe, Railway lo agregará automáticamente cuando conectes la BD

### PASO 3: Variables de Entorno Requeridas

En Railway Dashboard → Variables, asegúrate de tener:

```env
# ============ CRITICAL ============
DATABASE_URL = [generada automáticamente por Railway]
SECRET_KEY = [genera un valor fuerte]

# ============ REQUIRED ============
ENVIRONMENT = production
DEBUG = false
LOG_LEVEL = info

# ============ CORS ============
ALLOWED_ORIGINS = https://your-domain.com,https://www.your-domain.com

# ============ OPTIONAL ============
# Railway automáticamente proporciona:
# - PORT (por defecto 8000)
# - HOST (por defecto 0.0.0.0)
```

### PASO 4: Generar SECRET_KEY Segura

En tu terminal local:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copia el resultado y pégalo en `SECRET_KEY` en Railway.

### PASO 5: Deploy

```bash
git add app/main.py app/db/session.py .env.railway
git commit -m "fix: Improve database error handling for Railway deployment"
git push origin main
```

Railway redesplegará automáticamente ✨

---

## 🩺 VERIFICAR CONFIGURACIÓN

### 1. Revisar Logs en Railway
```
Railway Dashboard → Logs → Filter "Database"
```

Deberías ver:
```
Starting application in production environment
Database URL: postgresql://...
All routers loaded successfully
```

### 2. Probar Health Check
```bash
curl https://smartpcnube-production.up.railway.app/health

# Respuesta esperada:
{
  "status": "ok",
  "service": "MesaPass API",
  "environment": "production",
  "database_status": "connected"
}
```

### 3. Probar Health Deep
```bash
curl https://smartpcnube-production.up.railway.app/health/deep

# Respuesta esperada:
{
  "status": "ok",
  "service": "MesaPass API",
  "environment": "production",
  "database": "connected",
  "requirements": {
    "database_url_set": true,
    "debug_mode": false,
    "environment": "production"
  }
}
```

---

## ⚠️ PROBLEMAS COMUNES

### Error: "connection refused"
**Causa:** DATABASE_URL no está configurada
**Solución:** Revisa Railway Dashboard → Variables → DATABASE_URL

### Error: "could not connect to server"
**Causa:** Base de datos no está iniciada o URL es incorrecta
**Solución:** 
1. Revisa que la BD está running (Railway Dashboard)
2. Copia la DATABASE_URL correcta de Railway
3. Pega en Variables

### App arranca pero sin BD
**Causa:** BD opcional en desarrollo, obligatoria en producción
**Solución:** Configura correctamente DATABASE_URL en Railway

---

## 📝 CAMBIOS REALIZADOS

| Archivo | Cambio | Razón |
|---------|--------|-------|
| `app/main.py` | Lifespan más resiliente | No falla si BD no está disponible |
| `app/db/session.py` | Pool configuration | NullPool para Railway, regular para dev |
| `.env.railway` | Variables de ejemplo | Guía de configuración |

---

## 🔗 SIGUIENTES PASOS

1. **Configurar BD en Railway** (si aún no existe)
2. **Copiar DATABASE_URL** a Variables
3. **Configurar SECRET_KEY** y ALLOWED_ORIGINS
4. **Deploy** (git push)
5. **Verificar** con /health y /health/deep

---

## 📚 REFERENCIAS

- [Railway PostgreSQL Setup](https://docs.railway.app/databases/postgresql)
- [Railway Environment Variables](https://docs.railway.app/develop/variables)
- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)

