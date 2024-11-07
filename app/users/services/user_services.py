from ...database.connection import db
from ..models.user import User, UserInDb
from fastapi import HTTPException, status
from datetime import datetime
from ...firebase.token_service import set_user_role

async def fetch_user_by_id(user_id: str, current_user: dict):
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este usuario."
        )
    user = db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    return user

async def create_new_user(user: User, current_user: dict):
    user_id = current_user["user_id"]
    if user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autorizado para crear este recurso."
        )
    user_exist = await fetch_user_by_id(user.id, current_user)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya existe."
        )
    user_role = "administrator" if db.users.count_documents({}) == 0 else "client"
    try:
        await set_user_role(user_id, user_role)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al asignar rol al usuario."
        )
    user_model = user.model_dump(by_alias=True)
    user_db_model = UserInDb(
        _id=user_id,
        name=user_model["name"],
        email=user_model["email"],
        email_verified=user_model["email_verified"],
        picture=user_model["picture"],
        auth_method=current_user["provider"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        role=user_role,
        account_blocked=False,
        last_login=datetime.now()
    )
    try:
        result = db.users.insert_one(user_db_model.model_dump(by_alias=True))
        created_user = db.users.find_one({"_id": result.inserted_id})
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el usuario en la base de datos."
        )
    return created_user

#cmabiar el rol en el token
async def update_user_role(user_id: str, role: str):
    if role not in ["client", "administrator"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol inválido."
        )
    try:
        result = db.users.update_one(
            {"_id": user_id},
            {"$set": {"role": role, "updated_at": datetime.now()}}
        )
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el rol del usuario."
        ) 


async def fetch_all_users():
    try:
        users = db.users.find().to_list(length=100)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar los usuarios."
        )
    return users


async def set_user_block_status(user_id: str, blocked: bool):
    try:
        result = db.users.update_one(
            {"_id": user_id},
            {"$set": {"account_blocked": blocked, "updated_at": datetime.now()}}
        )
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )
        action = "bloqueado" if blocked else "desbloqueado"
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el estado de bloqueo del usuario."
        )
    return action

async def delete_user_from_db(user_id: str, current_user:dict):
    await fetch_user_by_id(user_id, current_user)
    try:
        result = db.users.delete_one({"_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado para eliminar."
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el usuario de la base de datos."
        )
    
"""
Por hacer:
Módulo de Usuarios
Historial de Acciones o Logs

Registrar las actividades importantes de los usuarios, como creación de cuenta, actualizaciones de perfil, cambios de rol, y eliminaciones de cuenta.
Filtrado, Paginación y Búsqueda Avanzada

Implementar filtros para listar usuarios según criterios como role, account_blocked, is_deleted, o created_at.
Paginación (limit, offset) para manejar grandes cantidades de usuarios en el listado.
Búsqueda avanzada por nombre, correo electrónico, u otros campos específicos.
Soft Delete

Añadir un campo como is_deleted o deleted_at para ocultar usuarios eliminados en lugar de borrarlos físicamente de la base de datos.
Agregar endpoints para listar y restaurar usuarios eliminados.
Manejo de Concurrencia

Implementar mecanismos para evitar conflictos al actualizar simultáneamente datos de un usuario, como los roles o el estado de bloqueo.
Documentación de Errores Detallada

Estandarizar respuestas de error y mejorar los mensajes de error para que sean informativos y consistentes. Usar un modelo de respuesta para capturar detalles del error, como código y mensaje.
Pruebas Unitarias y de Integración

Crear pruebas para cada endpoint del módulo de usuarios, cubriendo escenarios de éxito y error, incluyendo pruebas de concurrencia, paginación y filtros.
"""