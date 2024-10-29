from db.schemas.chatbot import Chatbot, Message
from db.client import db_client
from bson import ObjectId
from fastapi import HTTPException
from fastapi import Response

async def create_chatbot(chatbot: Chatbot):
    id_chatbot = db_client.chatbots.insert_one(chatbot.model_dump()).inserted_id
    if not id_chatbot:
        raise HTTPException(status_code=404, detail="Error al guardar el chatbot")
    return {"inserted_id": str(id_chatbot)}


async def create_script(chatbot_id: str):
    config_chatbot = db_client.chatbots.find_one({"_id":ObjectId(chatbot_id)})
    name=config_chatbot["name"]
    welcomeMessage=config_chatbot["setting"]["welcomeMessage"]
    position=config_chatbot["setting"]["position"]
    primaryColor=config_chatbot["setting"]["primaryColor"]
    secondaryColor=config_chatbot["setting"]["secondaryColor"]
    thirdColor=config_chatbot["setting"]["thirdColor"]
    fontSize=config_chatbot["setting"]["fontSize"]
    script = f"""(function() {{
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
        chatbotContainer.style.position = 'fixed';
        document.body.appendChild(chatbotContainer);
    }})();"""
    return Response(content=script, media_type="application/javascript")



async def generate_response(message: Message):
    return f"Message que enviaste fue {message}"