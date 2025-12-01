import os
from pymongo import MongoClient

# Leer variables de entorno
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "notas-db")

# Se crea la cadena de conexion
# Antiguo: MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
MONGO_URI = (f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
             f"{MONGO_DB}?authSource=admin"
             )

# Crear conexion
conn = MongoClient(MONGO_URI)
db = conn[MONGO_DB]
