from app.core.database import db

class Clase1Repository:
    
    #=======================================================
    #================ CRUD BASICO ==========================
    #=======================================================

    # ======= Listar todos los clase1 ========
    @staticmethod
    async def listar_todo(filtro: dict):
        resultados = await db.clase1.find(filtro).to_list(100)
        return resultados

    # ======= Crear clase1 ========
    @staticmethod
    async def crear(datos: dict):
        resultado = await db.clase1.insert_one(datos)
        return resultado.inserted_id


    # ======= Modificar clase1 ========
    @staticmethod
    async def modificar(id: str, datos: dict):
        await db.clase1.update_one({"_id": id}, {"$set": datos})
        return await db.clase1.find_one({"_id": id})


    # ======= Eliminar clase1 ========
    @staticmethod
    async def eliminar_por_id(id: str):
        resultado = await db.clase1.delete_one({"_id": id})
        return resultado.deleted_count > 0


    # ======= Obtener clase1 por id ========
    @staticmethod
    async def obtener_por_id(id: str):
        return await db.clase1.find_one({"_id": id})



    #===========================================================
    #================ CRUD DE SUBCLASE =========================
    #===========================================================

    # ======= Actualizar subclase, al ser una unica subclase modifica un unico apartado ========
    @staticmethod
    async def actualizar_subclase(id: str, subdatos: dict):
        await db.clase1.update_one(
            {"_id": id},
            {"$set": {"subclase": subdatos}}
        )
        return await db.clase1.find_one({"_id": id})



    #============================================================
    #================ CRUD DE LISTA =============================
    #============================================================


    # ======= Obtener email de lista de emails ========
    @staticmethod
    async def obtener_emails_de_listaEmails(id: str):
        resultado = await db.clase1.find_one(
            {"_id": id},
            {"listaEmails": 1, "_id": 0}
        )

        # Si no existe o no tiene resultado → devolver lista vacía
        if not resultado or "listaEmails" not in resultado:
            return []

        return resultado["listaEmails"]


    # ======= Agregar emails a listaEmails ========
    @staticmethod
    async def agregar_email(id: str, emailNuevo: str):
        await db.clase1.update_one(
            {"_id": id},
            {"$addToSet": {"listaEmails": emailNuevo}}
        )
        return await db.clase1.find_one({"_id": id})


    # ======= Modificar un email dentro de listaEmails ========
    @staticmethod
    async def modificar_email(id: str, emailAntiguo: str, emailNuevo: str):
        resultado = await db.clase1.update_one(
            {
                "_id": id,
                "listaEmails": emailAntiguo  # Busca el documento que contiene ese email en la lista
            },
            {
                "$set": {"listaEmails.$": emailNuevo}  # Reemplaza el valor encontrado por el nuevo
            }
        )

        # Si no encontró el email o no modificó nada → devolver None
        if resultado.matched_count == 0 or resultado.modified_count == 0:
            return None

        # Devuelve el documento actualizado
        return await db.clase1.find_one({"_id": id})


    # ======= Eliminar email de listaEmails ========
    @staticmethod
    async def eliminar_email(id: str, emailEliminar: str):
        resultado = await db.clase1.update_one(
            {"_id": id},
            {"$pull": {"listaEmails": emailEliminar}}
        )

        if resultado.matched_count == 0 or resultado.modified_count == 0:
            return None

        return await db.clase1.find_one({"_id": id})



    #===============================================================
    #================ CRUD DE LISTA DE SUBCLASE ====================
    #===============================================================
    
    # ======= Listar todas las subclases ========
    @staticmethod
    async def listar_subclases_de_lista(id: str):
        resultado = await db.clase1.find_one(
            {"_id": id},
            {"listaSubclase": 1, "_id": 0}
        )
        # Si no existe o no tiene resultado → devolver lista vacía
        if not resultado or "listaSubclase" not in resultado:
            return []
        listaSubclase = resultado["listaSubclase"]
        return listaSubclase


    # ======= Agregar subclase a listaSubclase ========
    @staticmethod
    async def agregar_subclase(id: str, subclaseNueva: dict):
        await db.clase1.update_one(
            {"_id": id},
            {"$addToSet": {"listaSubclase": subclaseNueva}}
        )
        return await db.clase1.find_one({"_id": id})


    # ======= Modificar subclase dentro de listaSubclase ========
    @staticmethod
    async def modificar_subclase_en_lista(id: str, subclaseAntigua: dict, subclaseNueva: dict):
        resultado = await db.clase1.update_one(
            {
                "_id": id,
                #"listaSubclase.id": id_subclase  # Busca dentro del array la subclase con ese id
                "listaSubclase": subclaseAntigua  # Busca el documento que contiene esa subclase en la lista
            },
            {
                "$set": {"listaSubclase.$": subclaseNueva}  # Reemplaza el valor encontrado por el nuevo
            }
        )
        # Si no encontró la subclase o no modificó nada → devolver None
        if resultado.matched_count == 0 or resultado.modified_count == 0:
            return None
        # Devuelve el documento actualizado
        return await db.clase1.find_one({"_id": id})


    # ======= Eliminar subclase de listaSubclase ========
    @staticmethod
    async def eliminar_subclase_de_lista(id: str, subclaseEliminar: dict):
        resultado = await db.clase1.update_one(
            {"_id": id},
            {"$pull": {"listaSubclase": subclaseEliminar}}
            #{"$pull": {"listaSubclase": {"id": id_subclase}}}  # Elimina por coincidencia de id interno
        )
        if resultado.matched_count == 0 or resultado.modified_count == 0:
            return None
        return await db.clase1.find_one({"_id": id})