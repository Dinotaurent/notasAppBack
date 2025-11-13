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


@nota.post("/notas", tags=["Nota"], response_model=Nota)
def create_nota(nota: Nota):
    new_nota = dict(nota)

    try:
        id = db["nota"].insert_one(new_nota).inserted_id
        nota = db["nota"].find_one({"_id": id})
        return notaEntity(nota)
    except PyMongoError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al momento de insertar la nota en bd: {str(e)}"
        )


@nota.put("/notas/{id}", tags=["Nota"], response_model=Nota)
def update_nota(id: str, nota: Nota):
    notaTemp = dict(nota)

    try:
        notaDb = db["nota"].find_one({"_id": ObjectId(id)})
        if not notaDb:
            raise HTTPException(
                status_code=404, detail="Nota no encontrada"
            )
        # Solo obtener los campos enviados
        incoming_data = nota.model_dump(exclude_unset=True)

        # Se trae la data de la db para tenerla de base
        updated_date = notaDb.copy()

        # Se actualiza lo que se envia
        for field, value in incoming_data.items():
            updated_date[field] = value

        # Con toda la data organizada se busca y se hace el update en la db
        resultado = db["nota"].find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": updated_date},
            return_document=True
        )
        return notaEntity(resultado)
    except PyMongoError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al modificar nota: {str(e)}"
        )


@nota.delete("/notas/{id}", tags=["Nota"])
def delete_nota(id: str):

    try:
        db["nota"].find_one_and_delete({"_id": ObjectId(id)})
        return Response(status_code=204)

    except PyMongoError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar nota: {str(e)}"
        )
