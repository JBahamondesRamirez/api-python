from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    email_verified: bool
    picture: str
    class Config:
        json_schema_extra = {
            "example": {
                "_id": "60a6c9f1c25b0c5f28d8b5f4",
                "name": "Juan Pérez",
                "email": "juan.perez@example.com",
                "email_verified": True,
                "picture": "https://example.com/avatar.jpg"
            }
        }
   
class UserInDb(User):
    auth_method: str
    created_at : datetime
    updated_at: datetime
    role:str
    account_blocked: bool
    last_login: datetime = None
    class Config:
        json_schema_extra = {
            "example": {
                "_id": "60a6c9f1c25b0c5f28d8b5f4",
                "name": "Juan Pérez",
                "email": "juan.perez@example.com",
                "email_verified": True,
                "picture": "https://example.com/avatar.jpg",
                "auth_method": "google",
                "created_at": "2023-11-06T14:00:00Z",
                "updated_at": "2023-11-07T10:00:00Z",
                "role": "client",
                "account_blocked": False,
                "last_login": "2023-11-07T08:30:00Z"
            }
        }
    