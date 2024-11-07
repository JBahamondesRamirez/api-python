from pydantic import BaseModel
from fastapi import Query
from datetime import datetime
from typing import Annotated


class ColorScheme(BaseModel):
    primary_color: Annotated[str, Query(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$')] 
    secondary_color: Annotated[str, Query(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$')] 
    third_color: Annotated[str, Query(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$')]
    class Config:
        json_schema_extra = {
            "example": {
                "primary_color": "#FFFFFF",
                "secondary_color": "#000000",
                "third_color": "#3498db"
            }
        }


class ChatbotSettings(BaseModel):
    welcome_message: str
    position: str
    colors: ColorScheme
    font_size_scale: float
    class Config:
        json_schema_extra = {
            "example": {
                "welcome_message": "¡Hola! ¿En qué puedo ayudarte hoy?",
                "position": "bottom-right",
                "colors": {
                    "primary_color": "#FFFFFF",
                    "secondary_color": "#000000",
                    "third_color": "#3498db"
                },
                "font_size_scale": 1.5
            }
        }


class Chatbot(BaseModel):
    client_id: str
    name_chatbot: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    description: str
    setting: ChatbotSettings
    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "60a6c9f1c25b0c5f28d8b5f4",
                "name_chatbot": "Asistente Virtual",
                "is_active": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "description": "Chatbot para Inacap",
                "setting": {
                    "welcome_message": "¡Hola! ¿En qué puedo ayudarte hoy?",
                    "position": "bottom-right",
                    "colors": {
                        "primary_color": "#FFFFFF",
                        "secondary_color": "#000000",
                        "third_color": "#3498db"
                    },
                    "font_size_scale": 1.5
                }
            }
        }
