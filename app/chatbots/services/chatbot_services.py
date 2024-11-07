from ...database.connection import db
from ..models.chatbot import Chatbot
from bson import ObjectId
from fastapi import HTTPException, status, Response
from datetime import datetime

async def find_chatbot_by_field(field: str, key: str):
    try:     
        chatbot = db.chatbots.find_one({field: ObjectId(key)}, {"_id": 0})
        if not chatbot:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chatbot no encontrado.")
        return chatbot
    except:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

async def create_chatbot(chatbot_data: Chatbot, current_user:dict):
    user_id = current_user["user_id"]
    if user_id != chatbot_data.client_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autorizado para crear este recurso."
        )
    chatbot_model_dump = chatbot_data.model_dump()
    chatbot_model_dump["created_at"] = datetime.now()
    chatbot_model_dump["updated_at"] = datetime.now()
    try:
        chatbot = db.chatbots.insert_one(chatbot_model_dump)
        chatbot_inserted = await find_chatbot_by_field("_id", str(chatbot.inserted_id))
        return chatbot_inserted
    except:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY)

async def update_chatbot(chatbot_id: str, update_chatbot_data: Chatbot, current_user:dict):
    current_chatbot = await find_chatbot_by_field("_id", ObjectId(chatbot_id))
    if current_chatbot["client_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar este chatbot."
        )
    chatbot_model_dump = update_chatbot_data.model_dump()
    chatbot_model_dump["updated_at"] = datetime.now()
    chatbot_model_dump["created_at"] = current_chatbot["created_at"]
    chatbot_model_dump["client_id"] = current_chatbot["client_id"]
    chatbot_model_dump["is_active"] = current_chatbot["is_active"]
    try:
        db.chatbots.find_one_and_replace({"_id": ObjectId(chatbot_id)}, chatbot_model_dump)
        chatbot_updated = await find_chatbot_by_field("_id", ObjectId(chatbot_id))
        return chatbot_updated
    except:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY)

async def delete_chatbot(chatbot_id: str, current_user:dict):
    current_chatbot = await find_chatbot_by_field("_id", ObjectId(chatbot_id))
    if current_chatbot["client_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este chatbot."
        )
    try:
        result = db.chatbots.find_one_and_delete({"_id": ObjectId(chatbot_id)})
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
    except:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY)

async def get_chatbots_by_client(client_id: str, current_user:dict):
    if client_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver los chatbots de otro cliente."
        )
    try:
        list_chatbots = list(db.chatbots.find({"client_id": client_id}))
        if not list_chatbots:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return [Chatbot(**chat) for chat in list_chatbots]
    except:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY)
    
async def set_chatbot_active_status(chatbot_id: str, is_active: bool):
    try:
        result = db.chatbots.find_one_and_update(
            {"_id": ObjectId(chatbot_id)},
            {"$set": {"is_active": is_active, "updated_at": datetime.now()}},
            return_document=True
        )
        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        action = "desbloqueado" if is_active else "bloqueado"
        return action
    except:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY)

#ajustar a todos los cambios
async def script_chatbot(chatbot_id: str):
    config_chatbot = db.chatbots.find_one({"_id":ObjectId(chatbot_id)})
    name=config_chatbot["name_chatbot"]
    welcomeMessage=config_chatbot["setting"]["welcome_message"]
    position=config_chatbot["setting"]["position"]
    primaryColor=config_chatbot["setting"]["colors"]["primary_color"]
    secondaryColor=config_chatbot["setting"]["colors"]["secondary_color"]
    thirdColor=config_chatbot["setting"]["colors"]["third_color"]
    fontSize=config_chatbot["setting"]["font_size_scale"]
    script = f"""(function() {{
        var linkIcons = document.createElement("link");
        linkIcons.rel = "stylesheet";
        linkIcons.href = "https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@48,400,0,0";
        document.head.appendChild(linkIcons);

        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = "http://localhost:8000/static/widget.css";
        document.head.appendChild(link);

        link.onload = function() {{
            var script = document.createElement('script');
            script.src = 'http://localhost:8000/static/widget.js';

            script.onload = function() {{
                chatbot.init({{
                    chatbot_id:'{chatbot_id}',
                    container: '#chatbot-container',
                    position: '{position}',
                    primaryColor: '{primaryColor}',
                    secondaryColor: '{secondaryColor}',
                    thirdColor: '{thirdColor}',
                    welcomeMessage: '{welcomeMessage}',
                    fontSize: '{fontSize}', 
                    name: '{name}'  
                }});
            }};
            document.body.appendChild(script);
        }};

        const chatbotContainer = document.createElement('div');
        chatbotContainer.id = 'chatbot-container';
        document.body.appendChild(chatbotContainer);
    }})();"""
    return Response(content=script, media_type="application/javascript")


"""
Historial de Acciones o Logs

Registrar actividades de los chatbots, como creación, actualización de estado (activo/inactivo), ediciones, y eliminaciones.
Filtrado, Paginación y Búsqueda Avanzada

Filtros para listar chatbots según client_id, is_active, created_at, o updated_at.
Implementar paginación (limit, offset) para mejorar la eficiencia en listados grandes.
Búsqueda avanzada según el nombre del chatbot u otros atributos específicos.
Soft Delete

Utilizar un campo como is_deleted o deleted_at para ocultar chatbots eliminados en lugar de eliminarlos permanentemente.
Incluir opciones para listar y restaurar chatbots eliminados.
Manejo de Concurrencia

Prevenir conflictos al actualizar simultáneamente datos de un chatbot, como el estado activo/inactivo o el contenido.
Documentación de Errores Detallada

Estandarizar respuestas de error con detalles sobre el tipo de error, código, y mensaje, para facilitar el diagnóstico de problemas.
Pruebas Unitarias y de Integración

Implementar pruebas para cada endpoint de chatbots, incluyendo escenarios de concurrencia, paginación, filtros y verificación de soft delete.
"""