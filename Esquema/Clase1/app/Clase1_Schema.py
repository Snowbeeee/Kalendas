from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from bson import ObjectId
from typing import Optional

class SubClase1(BaseModel):
    texto: str
    integer: int
    booleana: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "texto": "Ejemplo de texto",
                "integer": 42,
                "booleana": True
            }
        }
    }

class SubClase1Actualizar(BaseModel):
    texto: Optional[str]
    integer: Optional[int]
    booleana: Optional[bool]

    model_config = {
        "json_schema_extra": {
            "example": {
                "texto": "Texto actualizado",
                "integer": 99,
                "booleana": False
            }
        }
    }

class Clase1Crear(BaseModel):
    emailId: str = Field(alias="_id")
    texto: str = Field(..., min_length=5, max_length=50) # ... es obligatorio, min_length y max_length definen la longitud del string
    numero: int
    fecha: datetime = Field(default_factory=datetime.utcnow) #Por defecto toma la fecha y hora actual si no se proporcionan datos de entrada
    booleana: bool = Field(default=False) #Por defecto es False si no se proporcionan datos de entrada
    subclase: SubClase1 
    listaEmails: list[str] = Field(default_factory=list) #Por defecto es una lista vacía si no se proporcionan datos de entrada (Emails de otros usuarios))
    listaSubclase: list[SubClase1] = Field(default_factory=list) #Por defecto es una lista vacía si no se proporcionan datos de entrada

    model_config = {
        "populate_by_name": True,  # permite usar el alias _id y emailId
        "json_schema_extra": {
            "example": {
                "_id": "usuario@email.com",
                "texto": "Mi texto de prueba",
                "numero": 10,
                "fecha": "2025-11-11T12:00:00Z",
                "booleana": True,
                "subclase": {
                    "texto": "Subtexto",
                    "integer": 1,
                    "booleana": False
                },
                "listaEmails": ["otro@email.com"],
                "listaSubclase": [
                    {"texto": "Sub1", "integer": 2, "booleana": True}
                ]
            }
        }
    }

class Clase1Actualizar(BaseModel):
    texto: Optional[str] = Field(default=None, min_length=5, max_length=50)
    numero: Optional[int]
    fecha: Optional[datetime]
    booleana: Optional[bool]

    model_config = {
        "json_schema_extra": {
            "example": {
                "texto": "Nuevo texto",
                "numero": 20,
                "fecha": "2025-11-12T08:30:00Z",
                "booleana": False,
            }
        }
    }


class Clase1Respuesta(BaseModel):
    id: str = Field(alias="_id")
    texto: str
    numero: int
    fecha: datetime
    booleana: bool
    subclase: SubClase1
    listaEmails: list[str]
    listaSubclase: list[SubClase1]

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "usuario@email.com",
                "texto": "Respuesta de ejemplo",
                "numero": 100,
                "fecha": "2025-11-11T12:00:00Z",
                "booleana": True,
                "subclase": {"texto": "Subclase respuesta", "integer": 5, "booleana": False},
                "lista": ["email1@test.com", "email2@test.com"],
                "listaSubclase": [
                    {"texto": "Sub1", "integer": 2, "booleana": True}
                ]
            }
        }
    }
