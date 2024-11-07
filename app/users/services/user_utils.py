from ...database.connection import db
from datetime import datetime

async def update_last_login(user_id: str):
    db.users.update_one(
        {"_id": user_id},
        {"$set": {"last_login": datetime.now()}}
    )

#enviar correos electronicos, ya sea para los usuarios y los chatbots
#verificar si el usuario esta activo para que inicie sesion