from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from tech_challenge1.api.routes import books, stats, ml, metrics
from tech_challenge1.db.database import Base, engine
from tech_challenge1.api.routes.auth import auth_router
from tech_challenge1.api.routes.logs import router as logs_router
from tech_challenge1.utils.logging import logger
from prometheus_fastapi_instrumentator import Instrumentator

# meu Bearer: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MjYzMjE1N30.QJJ2ronni7rILy-JJDSL4TfmedBHGwgiPs6Dl7khbv8

app = FastAPI(
    title="Tech Challenge - API de Livros",
    version="1.0.0"
)

Instrumentator().instrument(app).expose(
    app,
    include_in_schema=False,
    should_gzip=True,
    endpoint="/api/v1/metrics"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas existentes
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["Stats"])
app.include_router(ml.router, prefix="/api/v1/ml", tags=["ML"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["Metrics"])
app.include_router(logs_router, prefix="/api/v1/logs", tags=["Logs"])




@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Requisição: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Resposta: {response.status_code}")
    return response


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Tech Challenge - API de Livros",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

@app.get("/api/v1/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}

@app.get("/", tags=["Root"])
def root():
    return {"message": "API de livros disponível em /api/v1/books"}

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("tech_challenge1.api.main:app", host="127.0.0.1", port=8000, reload=True)
