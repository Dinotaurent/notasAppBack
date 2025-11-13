import os
from pymongo import MongoClient

# Leer variables de entorno
# MONGO_USER = os.getenv("MONGO_USER")
# MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "dbprueba")

# Se crea la cadena de conexion
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

# Crear conexion
conn = MongoClient(MONGO_URI)
db = conn[MONGO_DB]
