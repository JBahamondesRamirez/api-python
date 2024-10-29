from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from fastapi import UploadFile




class User(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    email_verified: bool
    picture: str
    auth_method: str

class UserDb(User):
    created_at : datetime
    updated_at: datetime
    account_blocked: bool
