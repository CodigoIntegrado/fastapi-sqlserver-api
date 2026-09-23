from fastapi import FastAPI

from app.database import test_connection
from app.routes.produtos import router as produtos_router


app = FastAPI(
    title="Código Integrado API",
    description=(
        "API REST com Python, FastAPI e SQL Server "
        "criada no canal Código Integrado."
    ),
    version="1.0.0",
)


app.include_router(produtos_router)


@app.get(
    "/",
    tags=["Sistema"],
)
def home():
    return {
        "projeto": "Código Integrado",
        "mensagem": "API REST funcionando!",
        "status": "online",
    }


@app.get(
    "/health",
    tags=["Sistema"],
)
def health():
    database = test_connection()

    return {
        "api": "online",
        "database": {
            "connected": database["connected"],
            "database": database.get("database"),
        },
    }