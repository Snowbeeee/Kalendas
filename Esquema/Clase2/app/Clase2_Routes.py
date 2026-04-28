from fastapi import APIRouter, HTTPException, Path, Query, Body
from app.Clase2_Schema import Clase2Respuesta, Clase2Crear, Clase2Actualizar
from typing import Optional
from datetime import date
from app.Clase2_Service import Clase2Service

router = APIRouter(prefix="/Clase2", tags=[])
    
# ======= Listar todos los clase2 ========
@router.get(
    "/", tags=["CRUD"],
    response_model=list[Clase2Respuesta],
    status_code=200,
    responses={
        200: {"description": "Lista obtenida correctamente."},
        422: {"description": "Error en formato."},
        500: {"description": "Error interno del servidor."},
    },
)
async def listar_todo(    
    texto: Optional[str] = Query(None, description="texto que se desea filtrar (Ejemplo: prueba)"),
    numero: Optional[int] = Query(None, description="numero que se desea filtrar (Ejemplo: 22)"),
    fechaComienzo: Optional[date] = Query(None, description="Fecha de inicio del rango (YYYY-MM-DD) (Ejemplo:2025-10-27)"),
    fechaFinal: Optional[date] = Query(None, description="Fecha de fin del rango (YYYY-MM-DD) (Ejemplo: 2025-10-28)"),
    booleana: Optional[bool] = Query(None, description="booleana que se desea filtrar (Ejemplo: true)"),
    idCompartido: Optional[str] = Query(None, description="idCompartido que se desea filtrar (Ejemplo: usuario@email.com")
    ):

    return await Clase2Service.listar_todo(texto, numero, fechaComienzo, fechaFinal, booleana, idCompartido)



# ======= Crear clase2 ========
@router.post(
    "/", tags=["CRUD"],
    response_model=Clase2Respuesta,
    status_code=201,
    responses={
        201: {"description": "creado correctamente."},
        422: {"description": "Error de validación en los datos enviados."},
        500: {"description": "Error interno del servidor."},
    },
)
async def crear_comentario(datos: Clase2Crear):
    try:
        return await Clase2Service.crear(datos)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ======= Modificar clase2 ========
@router.put(
    "/{id}", tags=["CRUD"],
    response_model=Clase2Respuesta,
    status_code=200,
    responses={
        200: {"description": "Actualizado correctamente."},
        404: {"description": "clase2 no encontrada."},
        422: {"description": "Error de validación en los datos enviados."},
        500: {"description": "Error interno del servidor."},
    },
)
async def modificar(
    datos: Clase2Actualizar,
    id: str = Path(
        description="El ID (ObjectId de MongoDB) de la clase2 a modificar.",
        example="70fa1a01fee6ad04b5737208",
    ),
):
    try:
        return await Clase2Service.modificar(id, datos)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ======= Eliminar comentario ========
@router.delete(
    "/{id}", tags=["CRUD"],
    status_code=204,  # No Content
    responses={
        204: {"description": "clase2 eliminado correctamente."},
        404: {"description": "clase2 no encontrado."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def eliminar_por_id(
    id: str = Path(
        description="El ID (ObjectId de MongoDB) de la clase2 a eliminar.",
        example="70fa1a01fee6ad04b5737208",
    )
):
    try:
        await Clase2Service.eliminar_por_id(id)
        # No devolvemos contenido, cumple con el 204
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ======= Obtener comentario por id ========
@router.get(
    "/{id}", tags=["Lectura por ID"],
    response_model=Clase2Respuesta,
    status_code=200,
    responses={
        200: {"description": "clase2 encontrado correctamente."},
        404: {"description": "clase2 no encontrado."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def obtener_por_id(
    id: str = Path(
        description="El ID (ObjectId de MongoDB) de la clase2 a buscar.",
        example="70fa1a01fee6ad04b5737202",
    )
):
    try:
        return await Clase2Service.obtener_por_id(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

