from pydantic import BaseModel, Field
from fastapi import Query
from datetime import datetime
from typing import Annotated, Optional

class ColorScheme(BaseModel):
    primary_color: Annotated[str, Query(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$')] 
    secondary_color: Annotated[str, Query(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$')] 
    class Config:
        json_schema_extra = {
            "example": {
                "primary_color": "#FFFFFF",
                "secondary_color": "#000000",
            }
        }

class ChatbotSettings(BaseModel):
    welcome_message:str
    prompt:str
    instructions:str
    position:str
    font_size_scale: float
    colors: ColorScheme
    class Config:
        json_schema_extra = {
            "example": {
                "welcome_message": "¡Hola! ¿En qué puedo ayudarte hoy?",
                "prompt":"Response en base a este archivo",
                "instructions":"Response de manera corta y concisa",
                "position": "right",
                "font_size_scale": 1.5,
                "colors": {
                    "primary_color": "#FFFFFF",
                    "secondary_color": "#000000",
                    "third_color": "#3498db"
                },
            }
        }


class ChatbotDb(BaseModel):
    id: str = Field(alias="_id")
    client_id: str
    name_chatbot: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    setting: ChatbotSettings
    class Config:
        json_schema_extra = {
            "example": {
                "_id": "60a6c9f1c25b0c5f28d8b5f5",
                "client_id": "60a6c9f1c25b0c5f28d8b5f4",
                "name_chatbot": "Asistente Virtual",
                "description": "Chatbot para Inacap",
                "setting": {
                    "welcome_message": "¡Hola! ¿En qué puedo ayudarte hoy?",
                    "prompt":"Response en base a este archivo",
                    "instructions":"Response de manera corta y concisa",
                    "position": "bottom-right",
                    "colors": {
                        "primary_color": "#FFFFFF",
                        "secondary_color": "#000000",
                    },
                    "font_size_scale": 1.5
                }
            }
        }


class ChatbotResponse(BaseModel):
    id:str
    name:str
    script:str

