from ...database.connection import db
from ..models.chatbot import ChatbotDb, ChatbotResponse
from bson import ObjectId
from fastapi import HTTPException, status, Response
from datetime import datetime
from pymongo import ReturnDocument


def verify_permissions(chatbot_client_id, current_user_id):
    if chatbot_client_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción."
        )
    


async def find_chatbot_by_id(client_id:str, chatbot_id: str, current_user: dict):
    verify_permissions(client_id, current_user["user_id"]) 
    try:
        chatbot = db.chatbots.find_one({"_id": chatbot_id})
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot no encontrado."
            )
        return chatbot
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar el chatbot: {str(e)}"
        )

async def create_chatbot(chatbot_data: ChatbotDb, current_user:dict):
    verify_permissions(chatbot_data.client_id, current_user["user_id"])
    chatbot_model_dump = chatbot_data.model_dump(by_alias=True)
    chatbot_model_dump["is_active"] = True
    chatbot_model_dump["created_at"] = datetime.now()
    chatbot_model_dump["updated_at"] = datetime.now()
    try:
        result = db.chatbots.insert_one(chatbot_model_dump)
        chatbot_response = ChatbotResponse(
            id=str(result.inserted_id),
            name=chatbot_data.name_chatbot,
            script=f"<script src='http://localhost:8000/chatbot/{result.inserted_id}.js'></script>"
        ).model_dump()
        return chatbot_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al guardar el chatbot: {str(e)}" 
        )
    
async def update_chatbot(chatbot_id: str, update_chatbot_data: ChatbotDb, current_user:dict):
    current_chatbot = await find_chatbot_by_id(update_chatbot_data.client_id, chatbot_id, current_user)
    chatbot_model_dump = update_chatbot_data.model_dump(by_alias=True)
    chatbot_model_dump["updated_at"] = datetime.now()
    chatbot_model_dump["created_at"] = current_chatbot["created_at"]
    chatbot_model_dump["is_active"] = current_chatbot["is_active"]
    try:
        chatbot_updated = db.chatbots.find_one_and_replace({"_id": chatbot_id},chatbot_model_dump,return_document=ReturnDocument.AFTER)
        updated_id = chatbot_updated["_id"]
        chatbot_response = ChatbotResponse(
            id=str(updated_id),
            name=chatbot_updated["name_chatbot"],
            script=f"<script src='https://localhost:8000/chatbot/{updated_id}.js'></script>"
        ).model_dump()
        return chatbot_response
    except:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY)

async def delete_chatbot(client_id:str,chatbot_id: str, current_user:dict):
    await find_chatbot_by_id(client_id, chatbot_id, current_user)
    try:
        result = db.chatbots.find_one_and_delete({"_id": chatbot_id})
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
    except:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY)
    

async def get_chatbots_by_client(client_id: str, current_user: dict):
    if client_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver los chatbots de otro cliente."
        )
    try:
        list_chatbots = list(db.chatbots.find({"client_id": client_id}))
        if not list_chatbots:
            return []
        return [ChatbotDb(**chat) for chat in list_chatbots]
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail="Error al obtener los chatbots.")

    
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
    config_chatbot = db.chatbots.find_one({"_id":chatbot_id})
    if not config_chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    name=config_chatbot["name_chatbot"]
    welcomeMessage=config_chatbot["setting"]["welcome_message"]
    prompt = config_chatbot["setting"]["prompt"]
    instructions = config_chatbot["setting"]["instructions"]
    position=config_chatbot["setting"]["position"]
    primaryColor=config_chatbot["setting"]["colors"]["primary_color"]
    secondaryColor=config_chatbot["setting"]["colors"]["secondary_color"]
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
                console.log('Widget loaded');
            }};
            document.body.appendChild(script);

            script.onload = function() {{
                chatbot.init({{
                    chatbot_id:'{chatbot_id}',
                    container: '#chatbot-container',
                    prompt: '{prompt}',
                    instructions: '{instructions}',
                    position: '{position}',
                    primaryColor: '{primaryColor}',
                    secondaryColor: '{secondaryColor}',
                    welcomeMessage: '{welcomeMessage}',
                    fontSize: '{fontSize}', 
                    name: '{name}',
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
