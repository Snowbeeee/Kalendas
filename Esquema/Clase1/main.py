from fastapi import FastAPI
from app.Clase1_Routes import router as clase1_router


app = FastAPI(
    title="Parcial Server - Servicio de Clase1",
    version="1.0.0"
)

app.include_router(clase1_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)