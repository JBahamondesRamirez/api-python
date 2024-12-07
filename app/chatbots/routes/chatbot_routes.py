from fastapi import APIRouter, Depends, UploadFile, Form, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from ..models.chatbot import ChatbotDb, ChatbotResponse
from ..services.chatbot_services import create_chatbot,update_chatbot,delete_chatbot,get_chatbots_by_client,set_chatbot_active_status,script_chatbot, find_chatbot_by_id
from ...firebase.token_service import get_current_user, get_administrator_role
import asyncio
from pydantic import BaseModel


router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.get("/{chatbot_id}.js")
async def get_chatbot_script(chatbot_id: str):
    return await script_chatbot(chatbot_id)

@router.get("/get_chatbots_by_client")
async def get_chatbots_for_client(client_id: str, current_user:dict = Depends(get_current_user)):
    chatbots = await get_chatbots_by_client(client_id, current_user)
    return chatbots

#lista por ahora
@router.post("/create_chatbot", response_model=ChatbotResponse)
async def create_new_chatbot(chatbot: ChatbotDb, current_user:dict = Depends(get_current_user)):
    chatbot_created = await create_chatbot(chatbot, current_user)
    return JSONResponse(chatbot_created, status_code=status.HTTP_201_CREATED)


@router.get("/get_chatbot_by_id")
async def get_chatbot_by_id(client_id:str, chatbot_id: str, current_user: dict = Depends(get_current_user)):
    chatbot = await find_chatbot_by_id(client_id, chatbot_id, current_user)
    return chatbot

@router.put("/update_chatbot")
async def update_existing_chatbot(chatbot_id: str, update_data: ChatbotDb, current_user:dict = Depends(get_current_user)):
    chatbot_updated = await update_chatbot(chatbot_id, update_data, current_user)
    return JSONResponse(chatbot_updated, status_code=status.HTTP_200_OK)

@router.patch("/block_chatbot", dependencies=[Depends(get_administrator_role)])
async def change_chatbot_status(chatbot_id: str, is_active: bool):
    action = await set_chatbot_active_status(chatbot_id, is_active)
    return  action

@router.delete("/delete_chatbot")
async def remove_chatbot(client_id:str, chatbot_id: str, current_user:dict = Depends(get_current_user)):
    await delete_chatbot(client_id,chatbot_id, current_user)
    return {"status": "success"}









class AskRequest(BaseModel):
    pregunta: str
    chat_id:str

class AskRequest2(BaseModel):
    id: str
    question: str
    answer: str
    vote: str 


@router.post("/upload")
async def create_chatbot123(user_id: str = Form(...),chat_id: str = Form(...),pdf_file: UploadFile = None):
    await asyncio.sleep(2)
    return pdf_file


@router.post("/ask")
async def ask_question(chat_id: str, pregunta: str):
    """
    Recibe una pregunta, simula el procesamiento y devuelve un ID, pregunta y respuesta.
    """
    await asyncio.sleep(2) 
    mock_answer = f"Respuesta generada para: {pregunta}"
    return {
        "id": "1312",
        "question" : pregunta,
        "answer": mock_answer,
    }


@router.post("/ask2")
async def ask_question2(id: str, chat_id: str, vote: str, pregunta: str, respuesta: str):
    """
    Recibe un ID, pregunta, respuesta y un voto, y devuelve los datos como respuesta.
    """
    await asyncio.sleep(2)
    return {"status": "succes",}

