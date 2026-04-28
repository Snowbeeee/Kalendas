from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from bson import ObjectId
from typing import Optional

class Clase2Crear(BaseModel):
    #Id automático generado por la base de datos como ObjectId
    texto: str = Field(..., min_length=5, max_length=50) # ... es obligatorio, min_length y max_length definen la longitud del string
    numero: int
    fecha: datetime = Field(default_factory=datetime.utcnow) #Por defecto toma la fecha y hora actual si no se proporcionan datos de entrada
    booleana: bool = Field(default=False) #Por defecto es False si no se proporcionan datos de entrada
    idCompartido: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "texto": "Texto de prueba",
                "numero": 42,
                "fecha": "2025-11-11T10:30:00Z",
                "booleana": True,
                "idCompartido": "usuario@email.com"
            }
        }
    }

class Clase2Actualizar(BaseModel):
    texto: Optional[str] = Field(default=None, min_length=5, max_length=50)
    numero: Optional[int] = None
    fecha: Optional[datetime] = None
    booleana: Optional[bool] = None
    idCompartido: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "texto": "Actualización de comentario",
                "numero": 100,
                "fecha": "2025-11-11T11:00:00Z",
                "booleana": False,
                "idCompartido": "nuevo@email.com"
            }
        }
    }

class Clase2Respuesta(BaseModel):
    id: str = Field(alias="_id")
    texto: str
    numero: int
    fecha: datetime
    booleana: bool
    idCompartido: Optional[str] = None

    @model_validator(mode="before")
    def convertir_id_a_str(cls, values):
        if "_id" in values and isinstance(values["_id"], ObjectId):
            values["_id"] = str(values["_id"])
        return values


    model_config = {
        "from_attributes": True,
        "validate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "656f1a01fee6ad04b5737204",
                "texto": "Este es un comentario de prueba",
                "numero": 123,
                "fecha": "2025-11-11T12:00:00Z",
                "booleana": True,
                "idCompartido": "usuario@email.com"
            }
        }
    }