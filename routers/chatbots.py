from fastapi import APIRouter, Response
from db.schemas.chatbot import Chatbot, Message
from crud.chatbot import generate_response, create_script, create_chatbot

router = APIRouter(prefix="/chatbot",
                   tags=["Chatbot"])

@router.post("/create_chatbot")
async def create_chatbot_db(chatbot : Chatbot):
    chatbot_created = await create_chatbot(chatbot)
    return {"status": "success",
            "chatbot" : chatbot_created}

@router.get("/{chatbot_id}.js", response_class=Response)
async def create_script_chatbot(chatbot_id:str):
    return await create_script(chatbot_id)

@router.post("/generate-response")
async def message_test(message: Message):
    response = await generate_response(message)
    return {"response" : response}
