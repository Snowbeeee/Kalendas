from fastapi import FastAPI
from app.Clase2_Routes import router as clase2_router


app = FastAPI(
    title="Parcial Server - Servicio de Clase2",
    version="1.0.0"
)

app.include_router(clase2_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)