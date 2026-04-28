from app.core.database import db
from bson import ObjectId

class Clase2Repository:
    
    # ======= Listar todos los clase2 ========
    @staticmethod
    async def listar_todo(filtro: dict):
        resultados = await db.clase2.find(filtro).to_list(100)
        return resultados

    # ======= Crear clase2 ========
    @staticmethod
    async def crear(datos: dict):
        resultado = await db.clase2.insert_one(datos)
        return resultado.inserted_id


    # ======= Modificar clase2 ========
    @staticmethod
    async def modificar(id: ObjectId, datos: dict):
        await db.clase2.update_one({"_id": id}, {"$set": datos})
        return await db.clase2.find_one({"_id": id})


    # ======= Eliminar clase2 ========
    @staticmethod
    async def eliminar_por_id(id: ObjectId):
        resultado = await db.clase2.delete_one({"_id": id})
        return resultado.deleted_count > 0


    # ======= Obtener clase2 por id ========
    @staticmethod
    async def obtener_por_id(id: ObjectId):
        return await db.clase2.find_one({"_id": id})

