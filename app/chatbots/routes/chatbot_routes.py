from fastapi import APIRouter, Depends
from ..models.chatbot import Chatbot
from ..services.chatbot_services import (create_chatbot,update_chatbot,delete_chatbot,get_chatbots_by_client,set_chatbot_active_status,script_chatbot)
from ...firebase.token_service import get_current_user, get_administrator_role

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.get("/{chatbot_id}.js")
async def get_chatbot_script(chatbot_id: str):
    return await script_chatbot(chatbot_id)

@router.get("/get_chatbots_by_client")
async def get_chatbots_for_client(client_id: str, current_user:dict = Depends(get_current_user)):
    chatbots = await get_chatbots_by_client(client_id, current_user)
    return {"status": "success", "chatbots": chatbots}

@router.post("/create_chatbot")
async def create_new_chatbot(chatbot: Chatbot, current_user:dict = Depends(get_current_user)):
    chatbot_created = await create_chatbot(chatbot, current_user)
    return {"status": "success", "chatbot": chatbot_created}

@router.put("/update_chatbot")
async def update_existing_chatbot(chatbot_id: str, update_data: Chatbot, current_user:dict = Depends(get_current_user)):
    chatbot_updated = await update_chatbot(chatbot_id, update_data, current_user)
    return {"status": "success", "chatbot": chatbot_updated}

@router.patch("/block_chatbot", dependencies=[Depends(get_administrator_role)])
async def change_chatbot_status(chatbot_id: str, is_active: bool):
    action = await set_chatbot_active_status(chatbot_id, is_active)
    return {"status": "success", "action": action}

@router.delete("/delete_chatbot")
async def remove_chatbot(chatbot_id: str, current_user:dict = Depends(get_current_user)):
    await delete_chatbot(chatbot_id, current_user)
    return {"status": "success"}
