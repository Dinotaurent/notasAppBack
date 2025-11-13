def notaEntity(item) -> dict:
    return {
        "_id": str(item["_id"]),
        "titulo": str(item["titulo"]),
        "contenido": str(item["contenido"]),
    }


def notasEntity(entity) -> list:
    return [notaEntity(item) for item in entity]
