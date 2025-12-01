# ==============================================================================
# ETAPA 1: BUILDER (Instalación de Dependencias y Compilación)
# ==============================================================================

# Se usa la imagen base ligera de Debian (Bullseye) para Python.
FROM python:3.11-slim-bullseye AS builder

# ENVs para optimizar Pip y los logs en tiempo real.
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off

WORKDIR /app

# Instalar librerías de DESARROLLO (headers de compilación).
# Necesarias para compilar librerías nativas como psycopg2. Se limpia caché al finalizar.
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Optimización de caché de capas de Docker:
# Copiar primero solo dependencias.
COPY requirements.txt .
# Copiar el código fuente (incluye carpetas como 'src' y 'docs').
COPY . .

# Instalar todas las dependencias de Python.
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------------------------

# ==============================================================================
# ETAPA 2: RUNNER (Ejecución Mínima y Segura)
# ==============================================================================

# Misma base para evitar incompatibilidad de versiones.
FROM python:3.11-slim-bullseye AS runner

# Variables de Entorno y Rutas:
# PYTHONPATH=/app: Permite a Python encontrar módulos en carpetas internas (ej. 'src').
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar LIBRERÍAS DE EJECUCIÓN (RUNTIME) en el contenedor final.
# libpq5 es la librería cliente de Postgres necesaria para el runtime.
RUN apt-get update \
    && apt-get install --no-install-recommends -y libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar artefactos finales de la etapa 'builder':
# 1. Copiar librerías de Python compiladas.
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
# 2. Copiar ejecutables (Uvicorn, FastAPI) necesarios para el CMD.
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copiar el código fuente.
COPY . .

# Seguridad (Práctica Crítica):
# El proceso no se ejecuta como 'root'.
RUN adduser --system --group appuser
USER appuser

# Puerto que la aplicación escuchará (debe coincidir con el compose.yaml).
EXPOSE 8000

# Se ejecuta en el host 0.0.0.0 para ser accesible desde afuera del contenedor.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]