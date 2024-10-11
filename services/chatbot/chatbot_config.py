from db.models.chatbot import Config
from db.client import db_client
from bson import ObjectId
from fastapi import HTTPException

async def save_chatbot_config(config: Config):
    id_config = db_client.chatbots.insert_one(config.model_dump()).inserted_id
    config_chatbot = db_client.chatbots.find_one({"_id":ObjectId(id_config)})
    if not config_chatbot:
        raise HTTPException(status_code=404, detail="Error el guardar la configuración")
    return Config(**config_chatbot)