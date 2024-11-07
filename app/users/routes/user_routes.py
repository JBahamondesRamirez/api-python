from fastapi import APIRouter, Depends
from ..services.user_services import create_new_user, fetch_user_by_id, update_user_role, fetch_all_users, set_user_block_status, delete_user_from_db
from ..models.user import User
from ...firebase.token_service import get_current_user, get_administrator_role

router = APIRouter(prefix="/user",
                   tags=["user"])

@router.post("/create_user")
async def register_user(user : User, current_user : dict = Depends(get_current_user)):
    user_created = await create_new_user(user, current_user)  
    return {"status": "success", "user" : user_created}

@router.get("/exists_user/{user_id}")
async def check_user_existence(user_id: str, current_user:dict = Depends(get_current_user)):
    user = await fetch_user_by_id(user_id, current_user)
    return {"status": "success", "user" : user}

@router.patch("/update_role/{user_id}", dependencies=[Depends(get_administrator_role)])
async def modify_user_role(user_id:str, role:str):
    await update_user_role(user_id, role)
    return {"status" : "success", "role" : role}

@router.get("/list_users", dependencies=[Depends(get_administrator_role)])
async def retrieve_all_users():
    users = await fetch_all_users()
    return {"status" : "success", "users" : users}

@router.patch("/block_user/{user_id}", dependencies=[Depends(get_administrator_role)])
async def toggle_user_block_status(user_id:str, blocked:bool):
    action = await set_user_block_status(user_id, blocked)
    return {"status":"success", "action": action}

@router.delete("/delete_user")
async def remove_user(user_id:str, current_user:dict = Depends(get_current_user)):
    await delete_user_from_db(user_id, current_user)
    return {"status" : "success"}