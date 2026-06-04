# 📋 RAILWAY PRODUCTION DEPLOYMENT - GUÍA COMPLETA

## 🎯 Objetivo Final
Desplegar la aplicación FastAPI/MesaPass en Railway con base de datos PostgreSQL, manejo correcto de variables de entorno, y migraciones de base de datos ejecutadas de forma segura.

---

## 📌 ESTADO ACTUAL

### ✅ Completado
- [x] Dockerfile multi-stage optimizado
- [x] entrypoint.sh con proxy headers para Railway
- [x] app/main.py con lifespan management robusto
- [x] app/core/config.py con manejo de variables de entorno
- [x] app/db/session.py con pool connection robusto
- [x] requirements.txt con todas las dependencias (43 packages)
- [x] railway.json con configuración correcta
- [x] .env.railway con template de variables
- [x] railway-migrate.sh para ejecutar migraciones

### ⚠️ Pendiente
- [ ] Git commit y push
- [ ] Configurar variables en Railway Dashboard
- [ ] Ejecutar migraciones
- [ ] Validar health endpoints
- [ ] Pruebas de producción

---

## 🚀 PASOS A EJECUTAR

### 1️⃣ PREPARAR CÓDIGO LOCALMENTE

#### Verificar que todos los cambios están en su lugar
```bash
cd c:\Users\Lenovo\OneDrive\Escritorio\SMARTPC_NUBE\CODIGO\backend_plantilla

# Verificar archivos críticos
ls -la Dockerfile
ls -la entrypoint.sh
ls -la railway.json
ls -la .env.railway
ls -la railway-migrate.sh
ls -la app/main.py
ls -la app/core/config.py
ls -la app/db/session.py
```

#### Revisar que entrypoint.sh es ejecutable
```bash
chmod +x entrypoint.sh
chmod +x railway-migrate.sh
git add -A
git status  # Ver todos los cambios
```

---

### 2️⃣ COMMIT DE CAMBIOS

```bash
git add .

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

git push origin main
```

---

### 3️⃣ RAILWAY DASHBOARD - CONFIGURAR VARIABLES

**Ir a:** Railway → Tu Proyecto → Environment → Variables

Agregar las siguientes variables:

```
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
SKIP_DB_ON_STARTUP=false
DATABASE_URL=<obtener de Railway PostgreSQL plugin>
SECRET_KEY=<ejecutar: python -c "import secrets; print(secrets.token_urlsafe(32))">
ALLOWED_ORIGINS=https://tu-dominio.railway.app
APP_VERSION=1.0.0
APP_NAME=MesaPass API
```

**Donde obtener cada variable:**

| Variable | Fuente |
|----------|--------|
| `DATABASE_URL` | Railway → PostgreSQL Plugin → Connection String (copiar directamente) |
| `SECRET_KEY` | Ejecutar en terminal: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `ALLOWED_ORIGINS` | Tu dominio Railway (ej: `mesapass-prod.up.railway.app`) |

---

### 4️⃣ DESPLEGAR LA APP

Una vez subido el código a `main`, Railway detectará el cambio automáticamente y comenzará el build.

**Monitorear progreso en:** Railway Dashboard → Deployments

Logs esperados:
```
Step 1/12 : FROM python:3.12-slim as builder
Step 2/12 : WORKDIR /tmp
...
Step 12/12 : ENTRYPOINT ["/app/entrypoint.sh"]
✓ Built image successfully
✓ Pushing to registry...
✓ Deployment started
```

---

### 5️⃣ EJECUTAR MIGRACIONES

Una vez que el deployment inicial esté completo y el app arranque:

#### Opción A: Usando Railway CLI (RECOMENDADO)
```bash
# Si tienes railway CLI instalado
railway run bash railway-migrate.sh
```

#### Opción B: Manualmente desde tu máquina local
```bash
# Obtener DATABASE_URL desde Railway Dashboard
export DATABASE_URL="postgresql://postgres:password@host.railway.app:5432/railway_db"

# Ejecutar migraciones
cd starter-kit
alembic upgrade head
```

#### Opción C: Job en Railway (sin CLI)
En Railway Dashboard:
1. Crear un nuevo "Job" en el proyecto
2. Seleccionar el repositorio
3. Configurar comando: `bash railway-migrate.sh`
4. Ejecutar el job

---

### 6️⃣ VALIDAR DEPLOYMENT

#### Salud de la app (Health Check)
```bash
curl https://tu-dominio.railway.app/health
# Esperado: {"status": "OK", "environment": "production"}
```

#### Info de la app
```bash
curl https://tu-dominio.railway.app/info
# Esperado: {"app": "MesaPass API", "version": "1.0.0", "environment": "production"}
```

#### Logs de Railway
```bash
# Ver logs en tiempo real
railway logs
```

#### Logs esperados después de deployment
```
2026-06-04 10:15:23 INFO: Starting application in production environment
2026-06-04 10:15:23 INFO: Database URL configured: postgresql://postgres:...
2026-06-04 10:15:24 INFO: Database tables created/verified successfully
2026-06-04 10:15:24 INFO: CORS configured with origins: https://tu-dominio.railway.app
2026-06-04 10:15:24 INFO: All routers loaded successfully (54 routes)
2026-06-04 10:15:24 INFO: Application ready to receive requests
```

---

### 7️⃣ PROBAR ENDPOINTS

#### OpenAPI Documentation
```
https://tu-dominio.railway.app/docs
https://tu-dominio.railway.app/redoc
```

#### Prueba simple de un endpoint
```bash
# Si existe un endpoint de test
curl -X GET https://tu-dominio.railway.app/api/health \
  -H "Content-Type: application/json"
```

---

## 🔍 TROUBLESHOOTING

### Problema: App crashes con "Connection refused"
```
❌ psycopg2.OperationalError: connection to server at "localhost"
```

**Solución:**
1. Verificar que `DATABASE_URL` está configurada en Railway Dashboard
2. Ejecutar: `railway logs` para ver el error exacto
3. Asegurar que `ENVIRONMENT=production` está configurada

---

### Problema: ModuleNotFoundError en inicio
```
❌ ModuleNotFoundError: No module named 'qrcode'
```

**Solución:**
- Verificar que `requirements.txt` está actualizado (debe tener 43 packages)
- Si falta algo, agregar a `requirements.txt` y hacer push
- Railway reconstruirá automáticamente

---

### Problema: Logs vacíos o confusos
```bash
# Aumentar verbosidad de logs
# En Railway Dashboard → Variables
LOG_LEVEL=debug
```

---

### Problema: Migraciones fallando
```bash
# Ver estado actual de migraciones
alembic current

# Si hay conflicto, resetear:
alembic stamp head
alembic upgrade head
```

---

## 📊 MONITOREO

### Métricas a verificar regularmente
- ✅ Health check endpoint respondiendo
- ✅ CPU usage < 50%
- ✅ Memory usage < 200MB
- ✅ Deployment running (no crashed)
- ✅ Logs sin errores críticos

### Alert setup (Recomendado)
En Railway → Project Settings → Notifications:
- [x] Notify on deployment failure
- [x] Notify on deployment success

---

## 📝 CHECKLIST FINAL

- [ ] Git commit realizado y pushed
- [ ] Variables configuradas en Railway Dashboard
- [ ] DATABASE_URL conectando correctamente
- [ ] App deployada y arrancando sin errores
- [ ] Migraciones ejecutadas (`alembic upgrade head`)
- [ ] Health endpoint respondiendo 200 OK
- [ ] OpenAPI docs accesible
- [ ] Al menos un endpoint probado exitosamente
- [ ] Logs analizados y sin errores críticos
- [ ] Dominio custom configurado (si aplica)

---

## 🎉 ¿LISTO?

Una vez completados todos los pasos:

1. ✅ La app estará corriendo en `https://tu-dominio.railway.app`
2. ✅ Database conectada y migrada
3. ✅ Health checks respondiendo
4. ✅ Logs accesibles para debugging
5. ✅ Escalable automáticamente en Railway

---

## 📚 REFERENCIAS

- [Railway Documentation](https://docs.railway.app)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

---

**Documento generado:** 2026-06-04  
**Estado:** ✅ LISTO PARA PRODUCCIÓN
