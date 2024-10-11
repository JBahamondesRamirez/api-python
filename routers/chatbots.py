from fastapi import APIRouter, Response
from services.chatbot.chatbot_config import save_chatbot_config
from services.chatbot.chatbot_create import generate_chatbot
from fastapi.staticfiles import StaticFiles
from db.models.chatbot import Config, Message

router = APIRouter(prefix="/chatbot",
                   tags=["Chatbot"])


@router.post("/chatbot-config")
async def create_config(config : Config):
    chatbot_config = await save_chatbot_config(config)
    return {"status": "succes",
            "config" : chatbot_config}

@router.get("/{client_id}.js", response_class=Response)
async def create_chatbot(client_id:str):
    return await generate_chatbot(client_id)


@router.post("/mensajePrueba")
def menesajePrueba(message:Message):
    return {"response": f"La persona con este nombre {message.text} jamas lo pescara una mina "}