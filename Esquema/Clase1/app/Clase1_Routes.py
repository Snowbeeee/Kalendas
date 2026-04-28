from fastapi import APIRouter, HTTPException, Path, Query, Body
from app.Clase1_Schema import Clase1Respuesta, Clase1Crear, Clase1Actualizar, SubClase1Actualizar, SubClase1
from typing import Optional
from datetime import date
from app.Clase1_Service import Clase1Service

router = APIRouter(prefix="/Clase1", tags=[])

#=======================================================
#================ CRUD BASICO ==========================
#=======================================================
    
# ======= Listar todos los clase1 ========
@router.get(
    "/", tags=["CRUD"],
    response_model=list[Clase1Respuesta],
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
    subclase_texto: Optional[str] = Query(None, description="Texto de la subclase que se desea filtrar (Ejemplo: subtexto)"),
    subclase_integer: Optional[int] = Query(None, description="Integer de la subclase que se desea filtrar (Ejemplo: 5)"),
    subclase_booleana: Optional[bool] = Query(None, description="Booleana de la subclase que se desea filtrar (Ejemplo: false)"),
    listaEmails_filter: Optional[str] = Query(None, description="Lista de emails para buscar por emails"),
    listaSubclase_texto: Optional[str] = Query(None, description="Texto de la lista de subclases que se desea filtrar (Ejemplo: listasubtexto)")
    ):

    return await Clase1Service.listar_todo(texto, numero, fechaComienzo, fechaFinal, booleana, subclase_texto,subclase_integer, subclase_booleana, listaEmails_filter, listaSubclase_texto )



# ======= Crear clase1 ========
@router.post(
    "/", tags=["CRUD"],
    response_model=Clase1Respuesta,
    status_code=201,
    responses={
        201: {"description": "creado correctamente."},
        422: {"description": "Error de validación en los datos enviados."},
        500: {"description": "Error interno del servidor."},
    },
)
async def crear(datos: Clase1Crear):
    return await Clase1Service.crear(datos)


# ======= Modificar clase1 ========
@router.put(
    "/{id}", tags=["CRUD"],
    response_model=Clase1Respuesta,
    status_code=200,
    responses={
        200: {"description": "Actualizado correctamente."},
        404: {"description": "clase1 no encontrada."},
        422: {"description": "Error de validación en los datos enviados."},
        500: {"description": "Error interno del servidor."},
    },
)
async def modificar(
    datos: Clase1Actualizar,
    id: str = Path(
        description="El ID de la clase1 a modificar.",
        example="70fa1a01fee6ad04b5737208",
    ),
):
    try:
        return await Clase1Service.modificar(id, datos)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ======= Eliminar clase1 ========
@router.delete(
    "/{id}", tags=["CRUD"],
    status_code=204,  # No Content
    responses={
        204: {"description": "clase1 eliminado correctamente."},
        404: {"description": "clase1 no encontrado."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def eliminar_por_id(
    id: str = Path(
        description="El ID de la clase1 a eliminar.",
        example="70fa1a01fee6ad04b5737208",
    )
):
    try:
        await Clase1Service.eliminar_por_id(id)
        # No devolvemos contenido, cumple con el 204
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ======= Obtener clase1 por id ========
@router.get(
    "/{id}", tags=["Lectura por ID"],
    response_model=Clase1Respuesta,
    status_code=200,
    responses={
        200: {"description": "clase1 encontrado correctamente."},
        404: {"description": "clase1 no encontrado."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def obtener_por_id(
    id: str = Path(
        description="El ID de la clase1 a buscar.",
        example="usuario@email.com",
    )
):
    try:
        return await Clase1Service.obtener_por_id(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


#===========================================================
#================ CRUD DE SUBCLASE =========================
#===========================================================
# ======= Actualizar subclase, al ser una unica subclase modifica un unico apartado ========
@router.put(
    "/subclase/{subclaseId}", tags=["Actualizar subclase"],
    response_model=Clase1Respuesta,
    status_code=200,
    responses={
        200: {"description": "clase1 encontrado correctamente."},
        404: {"description": "clase1 no encontrado."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def actualizar_subclase(
    subclaseId: str = Path(
        description="El ID de la clase1 a buscar.",
        example="usuario@email.com",
    ),
    subdatos: dict = Body(
        description="Datos de la subclase a actualizar.",
        example={
            "texto": "Subtexto actualizado",
            "integer": 10,
            "booleana": True
        }
    )
):
    try:
        return await Clase1Service.actualizar_subclase(subclaseId, subdatos)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


#============================================================
#================ CRUD DE LISTA =============================
#============================================================

# ======= Obtener email de lista de emails ========
@router.get(
    "/listaEmails/{id}/", tags=["CRUD Lista Emails"],
    response_model=list[str],
    status_code=200,
    responses={
        200: {"description": "Lista de emails obtenida correctamente."},
        404: {"description": "clase1 no encontrado."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def obtener_emails_de_listaEmails(
    id: str = Path(
        description="El ID de la clase1 a buscar.",
        example="usuario@email.com",
    )
):
    try:
        return await Clase1Service.obtener_emails_de_listaEmails(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ======= Agregar emails a listaEmails ========
@router.post(
    "/listaEmails/{id}/", tags=["CRUD Lista Emails"],
    response_model=Clase1Respuesta,
    status_code=200,
    responses={
        200: {"description": "Email agregado correctamente."},
        404: {"description": "clase1 no encontrado."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def agregar_email(
    id: str = Path(
        description="El ID de la clase1 a buscar.",
        example="usuario@email.com",
    ),
    emailNuevo: str = Body(
        description="El email que se desea agregar a la lista.",
        example="nuevo@email.com"
    )
):
    try:
        return await Clase1Service.agregar_email(id, emailNuevo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ======= Modificar un email dentro de listaEmails ========
@router.put(
    "/listaEmails/{id}/", tags=["CRUD Lista Emails"],
    response_model=Clase1Respuesta,
    status_code=200,
    responses={
        200: {"description": "Email modificado correctamente."},
        404: {"description": "clase1 no encontrado."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def modificar_email(
    id: str = Path(
        description="El ID de la clase1 a buscar.",
        example="usuario@email.com",
    ),
    emailAntiguo: str = Query(None,
        description="El email que se desea modificar en la lista.",
        example="nuevo@email.com"
    ),
    emailNuevo: str = Query(None,
        description="El nuevo email que reemplazará al antiguo en la lista.",
        example="AAAAAAAAAA@email.com"
    )
):
    try:
        return await Clase1Service.modificar_email(id, emailAntiguo, emailNuevo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    


# ======= Eliminar email de listaEmails ========
@router.delete(
    "/listaEmails/{id}/", tags=["CRUD Lista Emails"],
    response_model=Clase1Respuesta,
    status_code=200,
    responses={
        200: {"description": "Email eliminado correctamente."},
        404: {"description": "clase1 no encontrado."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def eliminar_email(
    id: str = Path(
        description="El ID de la clase1 a buscar.",
        example="usuario@email.com",
    ),
    emailEliminar: str = Query(
        description="El email que se desea eliminar de la lista.",
        example="otro@email.com"
    )
):
    try:
        return await Clase1Service.eliminar_email(id, emailEliminar)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

#===============================================================
#================ CRUD DE LISTA DE SUBCLASE ====================
#===============================================================
    
# ======= Listar todas las subclases ========
@router.get(
    "/listaSubclase/{id}/",
    tags=["CRUD Lista Subclase"],
    response_model=list[SubClase1],
    status_code=200,
    responses={
        200: {"description": "Lista de subclases obtenida correctamente."},
        404: {"description": "Clase1 no encontrada."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def listar_subclases_de_lista(
    id: str = Path(
        description="El ID de la clase1 a buscar.",
        example="usuario@email.com",
    )
):
    try:
        return await Clase1Service.listar_subclases_de_lista(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



# ======= Agregar subclase a lista ========
@router.post(
    "/listaSubclase/{id}/",
    tags=["CRUD Lista Subclase"],
    response_model=Clase1Respuesta,
    status_code=200,
    responses={
        200: {"description": "Subclase agregada correctamente."},
        404: {"description": "Clase1 no encontrada."},
        422: {"description": "Datos inválidos o ID incorrecto."},
        500: {"description": "Error interno del servidor."},
    },
)
async def agregar_subclase_a_lista(
    subclaseNueva: SubClase1,
    id: str = Path(
        description="El ID de la clase1 donde se agregará la subclase.",
        example="usuario@email.com",
    )
):
    try:
        return await Clase1Service.agregar_subclase(id, subclaseNueva)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



# ======= Modificar subclase dentro de lista ========
@router.put(
    "/listaSubclase/{id}/",
    tags=["CRUD Lista Subclase"],
    response_model=Clase1Respuesta,
    status_code=200,
    responses={
        200: {"description": "Subclase modificada correctamente."},
        404: {"description": "Clase1 o subclase no encontrada."},
        422: {"description": "Datos inválidos o ID incorrecto."},
        500: {"description": "Error interno del servidor."},
    },
)
async def modificar_subclase_en_lista(
    subclaseAntigua: SubClase1,
    subclaseNueva: SubClase1,
    id: str = Path(
        description="El ID de la clase1 que contiene la subclase.",
        example="usuario@email.com",
    )
):
    try:
        return await Clase1Service.modificar_subclase_en_lista(id, subclaseAntigua, subclaseNueva)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



# ======= Eliminar subclase de lista ========
@router.delete(
    "/listaSubclase/{id}/",
    tags=["CRUD Lista Subclase"],
    response_model=Clase1Respuesta,
    status_code=200,
    responses={
        200: {"description": "Subclase eliminada correctamente."},
        404: {"description": "Clase1 o subclase no encontrada."},
        422: {"description": "ID con formato inválido."},
        500: {"description": "Error interno del servidor."},
    },
)
async def eliminar_subclase_de_lista(
    subclaseEliminar: SubClase1,
    id: str = Path(
        description="El ID de la clase1 de la que se eliminará la subclase.",
        example="usuario@email.com",
    )
):
    try:
        return await Clase1Service.eliminar_subclase_de_lista(id, subclaseEliminar)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))