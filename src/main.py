from fastapi import FastAPI, Response
from docs import tags_metadata


app = FastAPI(
    title="Notas app v2",
    description="Microservicio de notas",
    version="0.0.1",
    openapi_tags=tags_metadata
)

# Status


@app.get("/status", tags=["get-status"])
def get_status():
    return Response(status_code=200)
