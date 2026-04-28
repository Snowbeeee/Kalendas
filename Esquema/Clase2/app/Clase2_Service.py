from typing import Optional
from datetime import datetime, date
from zoneinfo import ZoneInfo
from app.Clase2_Repository import Clase2Repository
from app.Clase2_Schema import Clase2Crear, Clase2Actualizar, Clase2Respuesta
from bson import ObjectId
from app.core.config import settings
import httpx

CLASE1_URL = settings.CLASE1_URL

class Clase2Service():
   
    # ======= Listar todos los clase2 ========
    @staticmethod
    async def listar_todo(
            texto: Optional[str],
            numero: Optional[int],
            fechaComienzo: Optional[date],
            fechaFinal: Optional[date],
            booleana: Optional[bool],
            idCompartido: Optional[str] = None
        ):

        filtro = {}

        # Filtrar por texto partcial, si contiene una parte sale
        if texto:
            filtro["texto"] = {"$regex": texto, "$options": "i"}

        if idCompartido: #ID compartido exacto
            filtro["idCompartido"] = idCompartido

        # Filtrar por numero exacto
        if numero:
            filtro["numero"] = numero

        # Filtrar por booleana exacta si es true o false, las None no las muestra
        if booleana is not None:
            filtro["booleana"] = booleana

        # Filtrar por rango de fechas
        if fechaComienzo or fechaFinal:
            filtro["fecha"] = {}
            if fechaComienzo:
                filtro["fecha"]["$gte"] = datetime.combine(fechaComienzo, datetime.min.time(), tzinfo=ZoneInfo("Europe/Madrid"))
            if fechaFinal:
                filtro["fecha"]["$lte"] = datetime.combine(fechaFinal, datetime.max.time(), tzinfo=ZoneInfo("Europe/Madrid"))
    
        return await Clase2Repository.listar_todo(filtro)


    # ======= Crear clase2 ========
    @staticmethod
    async def crear(datos: Clase2Crear):
        # si viene un id compartido, comprobar que existe en Clase1
        if datos.idCompartido:
                async with httpx.AsyncClient(timeout=5.0) as cliente:
                    respuesta = await cliente.get(f"{CLASE1_URL}/{datos.idCompartido}")
            
                    # Si la respuesta no es 200, el idCompartido no existe
                    if respuesta.status_code != 200:
                        raise ValueError("El idCompartido no existe en Clase1")

        # Si todo va bien, continuar con la creación
        datos_dict = datos.model_dump()
        resultadoId = await Clase2Repository.crear(datos_dict)
                
        # Construir el objeto para la respuesta, convirtiendo a ComentarioResponse
        datosRespuesta = {"_id": resultadoId, **datos_dict}
        return Clase2Respuesta(**datosRespuesta)



    # ======= Modificar clase2 ========
    @staticmethod
    async def modificar(id: str, datos: Clase2Actualizar):
        try:
            objetoId = ObjectId(id)
        except:
            raise ValueError("ID de la clase2 no válida") # Si el id no es un ObjectId válido, lanza un error 404

        datos_dict = {k: v for k, v in datos.model_dump().items() if v is not None} # Elimina los campos que son None

        if not datos_dict:
            raise ValueError("No se proporcionaron datos para actualizar la clase2") # Si no hay datos para actualizar, lanza un error 404

        # Si viene idCompartido, comprobar que existe en Clase1
        if "idCompartido" in datos_dict:
            if datos_dict["idCompartido"] == "borrar":
                # Continuar sin validar, se usará para poner a None
                datos_dict["idCompartido"] = None
            elif datos_dict["idCompartido"]:
                # Si viene un valor real, validar que exista en Clase1
                async with httpx.AsyncClient(timeout=5.0) as cliente:
                    respuesta = await cliente.get(f"{CLASE1_URL}/{datos_dict['idCompartido']}")
                    if respuesta.status_code != 200:
                        raise ValueError("El idCompartido no existe en Clase1")


        resultado = await Clase2Repository.modificar(objetoId, datos_dict)
        return Clase2Respuesta(**resultado)



    # ======= Eliminar clase2 ========
    @staticmethod
    async def eliminar_por_id(id: str):
        try:
            objetoId = ObjectId(id)
        except:
            raise ValueError("ID de clase2 no válida") # Si el id no es un ObjectId válido, lanza un error 404

        eliminado = await Clase2Repository.eliminar_por_id(objetoId)
        if not eliminado:
            raise ValueError("clase2 no encontrada o no se pudo eliminar") # Si no se pudo eliminar, lanza un error 404



    # ======= Obtener clase2 por id ========
    @staticmethod
    async def obtener_por_id(id: ObjectId):
        try:
            objetoId = ObjectId(id)
        except:
            raise ValueError("ID de clase2 no válido") # Si el id no es un ObjectId válido, lanza un error 404

        resultado = await Clase2Repository.obtener_por_id(objetoId)
        if not resultado:
            raise ValueError("clase2 no encontrada") # Si no se encuentra el comentario, lanza un error 404

        return Clase2Respuesta(**resultado)