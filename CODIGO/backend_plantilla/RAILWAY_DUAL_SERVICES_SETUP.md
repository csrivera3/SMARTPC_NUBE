# 🚀 Railway - Configuración de Dos Servicios (Frontend + Backend)

## 📋 Resumen

Este proyecto contiene:
- **Frontend**: Next.js en `starter-kit/starter-kit/`
- **Backend**: FastAPI en `starter-kit/starter-kit/` (mismo directorio, ambos servicios)

Para Railway: debes crear **dos servicios separados** en el mismo repositorio.

---

## 🎯 Configuración del Servicio 1: FRONTEND (Next.js)

### Paso 1: En Railway Dashboard
1. Ve a tu proyecto en Railway
2. Click en **"New"** → **"Service"** → **"GitHub Repo"**
3. Selecciona este repositorio

### Paso 2: Configurar el Servicio Frontend

| Campo | Valor |
|-------|-------|
| **Service Name** | `frontend` o `wonderful-friendship` |
| **Root Directory** | `/starter-kit/starter-kit` |
| **Dockerfile Path** | `Dockerfile` |

### Paso 3: Variables de Entorno (si es necesario)
```
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://tu-backend.railway.app
```

---

## 🔧 Configuración del Servicio 2: BACKEND (FastAPI)

### Paso 1: En Railway Dashboard
1. En tu proyecto, click en **"New"** → **"Service"** → **"GitHub Repo"**
2. Selecciona el mismo repositorio

### Paso 2: Configurar el Servicio Backend

| Campo | Valor |
|-------|-------|
| **Service Name** | `backend` |
| **Root Directory** | `/` (raíz del repositorio) |
| **Dockerfile Path** | `Dockerfile.fastapi` |

### Paso 3: Variables de Entorno
```
DATABASE_URL=postgresql://...
PORT=8000
ENVIRONMENT=production
```

---

## 📂 Estructura de Archivos

```
backend_plantilla/ (raíz del repo)
│
├── Dockerfile.fastapi ← Para Backend (apunta a Dockerfile.fastapi)
├── entrypoint.sh
├── Dockerfile ← VIEJO (puedes eliminar o renombrar)
│
└── starter-kit/starter-kit/
    ├── Dockerfile ← Para Frontend (Next.js)
    ├── package.json ← Next.js
    ├── next.config.mjs
    ├── src/ ← Frontend React
    ├── requirements.txt ← Backend Python
    ├── app/ ← Backend Python
    └── migrations/ ← Backend Python
```

---

## 🔗 Conectar Servicios

### En Railway:
1. **Frontend** necesita saber la URL del Backend:
   - Variable: `NEXT_PUBLIC_API_URL=https://backend-service-url`

2. **Backend** necesita estar expuesto:
   - Puerto: `8000` (automático en Railway)
   - Generar URL pública: Railway crea automáticamente

---

## ✅ Después de Crear los Servicios

### En Railway:
1. El frontend debería detectar automáticamente como **Next.js**
2. El backend debería detectar automáticamente como **Python (FastAPI)**
3. Ambos construirán e desplegarán independientemente

### URLs Generadas:
- Frontend: `https://wonderful-friendship.railway.app` (o tu nombre de servicio)
- Backend: `https://backend.railway.app` (o tu nombre de servicio)

---

## 🚨 Solución de Problemas

### Si Railway aún detecta como Python en el Frontend:
- ❌ **NO** uses `railway.json` en la raíz para este servicio
- ✅ Elimina el `railway.json` o especifica explícitamente el Dockerfile
- ✅ En Railway UI, configura: **Dockerfile Path** = `Dockerfile`

### Si el Backend no encuentra las dependencias:
- ✅ Verifica que `starter-kit/starter-kit/requirements.txt` existe
- ✅ Dockerfile.fastapi debe apuntar correctamente a `COPY starter-kit/starter-kit/requirements.txt`

---

## 📝 Comandos Útiles Locales

### Construir y probar Frontend localmente:
```bash
cd starter-kit/starter-kit
docker build -t mesapass-frontend .
docker run -p 3000:3000 mesapass-frontend
```

### Construir y probar Backend localmente:
```bash
docker build -f Dockerfile.fastapi -t mesapass-backend .
docker run -p 8000:8000 -e DATABASE_URL=... mesapass-backend
```

---

## 🎯 Orden de Despliegue Recomendado

1. ✅ Despliega primero el **Backend** (en Railway)
2. ✅ Obtén su URL pública
3. ✅ Actualiza `NEXT_PUBLIC_API_URL` en el Frontend
4. ✅ Despliega el **Frontend**

---

## 📌 Nota Importante

Ambos servicios comparten la carpeta `starter-kit/starter-kit/` pero son **completamente independientes**:
- El Dockerfile de Frontend solo copia `src/`, `package.json` y `.next/`
- El Dockerfile de Backend solo copia `app/`, `requirements.txt` y migraciones
- Cada uno construye su propio contenedor de forma aislada
