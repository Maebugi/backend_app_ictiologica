from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.auth import router as auth_router
from app.api.v1.user import router as users_router
from app.api.v1.species import router as species_router
from app.api.v1.salidas import router as salidas_router
from app.api.v1.ocurrencias import router as ocurrencias_router
from app.api.v1.mediciones import router as mediciones_router
from app.api.v1.evidencias import router as evidencias_router

app = FastAPI(
    title="API Ictiológica",
    version="1.0.0"
)

app.include_router(users_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(species_router, prefix="/api/v1")
app.include_router(salidas_router, prefix="/api/v1")
app.include_router(ocurrencias_router, prefix="/api/v1")
app.include_router(mediciones_router, prefix="/api/v1")
app.include_router(evidencias_router, prefix="/api/v1")

app.mount("/storage", StaticFiles(directory="storage"), name="storage")