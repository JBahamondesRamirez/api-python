from firebase_admin import auth
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from ..users.services.user_utils import update_last_login
import asyncio

security = HTTPBearer()

async def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(security)):
    await asyncio.sleep(2)
    try:
        token = credentials.credentials
        decode_token = auth.verify_id_token(token)
        user_id = decode_token["user_id"]
        provider = decode_token["firebase"]["sign_in_provider"]
        role = decode_token.get("role")
        await update_last_login(user_id)
        return {"user_id": user_id, "role": role, "provider": provider}
    except:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    

async def get_user_role(role:str,credentials: HTTPAuthorizationCredentials):
    user = await get_current_user(credentials)
    if user["role"] != role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

async def get_administrator_role(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await get_user_role("administrator", credentials)

async def set_user_role(user_id:str, role:str):
    try:
        auth.set_custom_user_claims(user_id, {"role" : role})
        return role
    except:
        raise HTTPException(status.HTTP_304_NOT_MODIFIED)