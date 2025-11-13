from fastapi import APIRouter, HTTPException, Response
from config.db import db
from schemas.nota import notaEntity, notasEntity
from models.nota import Nota
from pymongo.errors import PyMongoError
from bson import ObjectId


# Se instancia el router
nota = APIRouter()


# Endpoints
@nota.get("/notas", tags=["Nota"])
def get_all_notas(page: int = 1, limit: int = 10):

    try:
        skip = (page - 1) * limit
        notas = list(db["nota"].find().skip(skip).limit(limit))
        total = db["nota"].count_documents({})
        return {
            "data": notasEntity(notas),
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit
        }
    except PyMongoError as e:
        raise HTTPException(
            status_code=500, detail=f"Error de conexion con la db: {str(e)}"
        )


@nota.get("/notas/{id}", tags=["Nota"], response_model=Nota)
def get_nota_by_id(id: str):

    try:
        nota = db["nota"].find_one({"_id": ObjectId(id)})
        if not nota:
            raise HTTPException(
                status_code=404, detail="Nota no encontrada"
            )
        return notaEntity(nota)
    except PyMongoError as e:
        raise HTTPException(
            status_code=500, detail=f"Error de conexion con la db: {str(e)}"
        )
