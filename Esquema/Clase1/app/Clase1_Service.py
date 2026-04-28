from typing import Optional
from datetime import datetime, date
from zoneinfo import ZoneInfo
from app.Clase1_Repository import Clase1Repository
from app.Clase1_Schema import Clase1Crear, Clase1Actualizar, Clase1Respuesta, SubClase1
from bson import ObjectId
from app.core.config import settings
import httpx

CLASE2_URL = settings.CLASE2_URL

class Clase1Service():

    #=======================================================
    #================ CRUD BASICO ==========================
    #=======================================================
   
    # ======= Listar todos los clase1 ========
    @staticmethod
    async def listar_todo(
            texto: Optional[str],
            numero: Optional[int],
            fechaComienzo: Optional[date],
            fechaFinal: Optional[date],
            booleana: Optional[bool],
            subclase_texto: Optional[str],
            subclase_integer: Optional[int],
            subclase_booleana: Optional[bool],
            listaEmails_filter: Optional[str],
            listaSubclase_texto: Optional[str]
        ):

        filtro = {}

        # Filtrar por texto partcial, si contiene una parte sale
        if texto:
            filtro["texto"] = {"$regex": texto, "$options": "i"}

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

        if subclase_texto:
            filtro["subclase.texto"] = {"$regex": subclase_texto, "$options": "i"}

        if subclase_integer is not None:
            filtro["subclase.integer"] = subclase_integer

        if subclase_booleana is not None:
            filtro["subclase.booleana"] = subclase_booleana

        if listaEmails_filter:
            filtro["listaEmails"] = listaEmails_filter

        if listaSubclase_texto:
            filtro["listaSubclase.texto"] = {"$regex": listaSubclase_texto, "$options": "i"}
    
        return await Clase1Repository.listar_todo(filtro)


    # ======= Crear clase1 ========
    @staticmethod
    async def crear(datos: Clase1Crear):
        datos_dict = datos.model_dump(by_alias=True)
        resultadoId = await Clase1Repository.crear(datos_dict)
                
        # Construir el objeto para la respuesta, convirtiendo a ComentarioResponse
        datosRespuesta = {"_id": resultadoId, **datos_dict}
        return Clase1Respuesta(**datosRespuesta)



    # ======= Modificar clase1 ========
    @staticmethod
    async def modificar(id: str, datos: Clase1Actualizar):
        datos_dict = {k: v for k, v in datos.model_dump().items() if v is not None} # Elimina los campos que son None

        if not datos_dict:
            raise ValueError("No se proporcionaron datos para actualizar la clase1") # Si no hay datos para actualizar, lanza un error 404

        resultado = await Clase1Repository.modificar(id, datos_dict)
        return Clase1Respuesta(**resultado)



    # ======= Eliminar clase1 ========
    @staticmethod
    async def eliminar_por_id(id: str):
        # 3️⃣ Poner idCompartido a null en Clase2
        try:
            async with httpx.AsyncClient(timeout=5.0) as cliente:
                resp_listar = await cliente.get(f"{CLASE2_URL}/", params={"idCompartido": str(id)})
        except httpx.RequestError as exc:
            # Si no conecta, no borra la Clase1
            raise ValueError(f"No se pudo conectar con el microservicio Clase2: {str(exc)}")

        # 2️⃣ Comprobar si la respuesta fue exitosa
        if resp_listar.status_code != 200:
            raise ValueError(f"No se pudo conectar con el microservicio Clase2")

        lista_clase2 = resp_listar.json()
        if lista_clase2:
            async with httpx.AsyncClient(timeout=10.0) as cliente:
                for clase2 in lista_clase2:
                    await cliente.put(
                        f"{CLASE2_URL}/{clase2['_id']}",
                        json={"idCompartido": "borrar"}
                    )

        eliminado = await Clase1Repository.eliminar_por_id(id)
        if not eliminado:
            raise ValueError("clase1 no encontrada o no se pudo eliminar") # Si no se pudo eliminar, lanza un error 404



    # ======= Obtener clase1 por id ========
    @staticmethod
    async def obtener_por_id(id: str):
        resultado = await Clase1Repository.obtener_por_id(id)
        if not resultado:
            raise ValueError("clase1 no encontrada") # Si no se encuentra el comentario, lanza un error 404

        return Clase1Respuesta(**resultado)
    

    #===========================================================
    #================ CRUD DE SUBCLASE =========================
    #===========================================================


    # ======= Actualizar subclase ========
    @staticmethod
    async def actualizar_subclase(id: str, subdatos: dict):
        resultado = await Clase1Repository.actualizar_subclase(id, subdatos)
        if not resultado:
            raise ValueError("clase1 no encontrada") # Si no se encuentra el comentario, lanza un error 404
        
        return Clase1Respuesta(**resultado)
    


    #============================================================
    #================ CRUD DE LISTA =============================
    #============================================================


    # ======= Agregar email a lista ========
    @staticmethod
    async def agregar_email(id: str, emailNuevo: str):
        resultado = await Clase1Repository.agregar_email(id, emailNuevo)
        return Clase1Respuesta(**resultado)
    

    
    # ======= Obtener email de lista de emails ========
    @staticmethod
    async def obtener_emails_de_listaEmails(id: str):
        listaEmails = await Clase1Repository.obtener_emails_de_listaEmails(id)
        return listaEmails
    

    # ======= Modificar email en listaEmails ========
    @staticmethod
    async def modificar_email(id: str, emailAntiguo: str, emailNuevo: str):
        resultado = await Clase1Repository.modificar_email(id, emailAntiguo, emailNuevo)
        if not resultado:
            raise ValueError("clase1 no encontrada ") # Si no se encuentra el comentario, lanza un error 404
        return Clase1Respuesta(**resultado)
    

    # ======= Eliminar email de listaEmails ========
    @staticmethod
    async def eliminar_email(id: str, emailEliminar: str):
        resultado = await Clase1Repository.eliminar_email(id, emailEliminar)
        if not resultado:
            raise ValueError("clase1 no encontrada ") # Si no se encuentra el comentario, lanza un error 404
        return Clase1Respuesta(**resultado)


    #===============================================================
    #================ CRUD DE LISTA DE SUBCLASE ====================
    #===============================================================


    # ======= Listar todas las subclases ========
    @staticmethod
    async def listar_subclases_de_lista(id: str):
        listaSubclase = await Clase1Repository.listar_subclases_de_lista(id)
        if listaSubclase is None:
            raise ValueError("clase1 no encontrada") # Si no se encuentra el comentario, lanza un error 404
        return listaSubclase
    

    # ======= Agregar subclase a lista ========
    @staticmethod
    async def agregar_subclase(id: str, subclaseNueva: SubClase1):
        resultado = await Clase1Repository.agregar_subclase(id, subclaseNueva.model_dump())
        if not resultado:
            raise ValueError("clase1 no encontrada ") # Si no se encuentra el comentario, lanza un error 404
        return Clase1Respuesta(**resultado)
    

    # ======= Modificar subclase dentro de lista ========
    @staticmethod
    async def modificar_subclase_en_lista(id: str, subclaseAntigua: SubClase1, subclaseNueva: SubClase1):
        resultado = await Clase1Repository.modificar_subclase_en_lista(id, subclaseAntigua.model_dump(), subclaseNueva.model_dump())
        if not resultado:
            raise ValueError("clase1 no encontrada o subclase inexistente") # Si no se encuentra el comentario, lanza un error 404
        return Clase1Respuesta(**resultado)
    
    # ======= Eliminar subclase de lista ========
    @staticmethod
    async def eliminar_subclase_de_lista(id: str, subclaseEliminar: SubClase1):
        resultado = await Clase1Repository.eliminar_subclase_de_lista(id, subclaseEliminar.model_dump())
        if not resultado:
            raise ValueError("clase1 no encontrada o subclase inexistente") # Si no se encuentra el comentario, lanza un error 404
        return Clase1Respuesta(**resultado)