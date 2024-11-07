from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.users.routes.user_routes import router as user_routes
from app.chatbots.routes.chatbot_routes import router as chatbot_routes
from app.sessions.routes.sessions_routes import router as sessions_routes
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.firebase.firebase_service import initialice_firebase

app = FastAPI()
initialice_firebase()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(chatbot_routes)
app.include_router(user_routes)
#app.include_router(sessions_routes)

#Crear un endpoint de salud (/health o /status) para verificar el funcionamiento de la API y del acceso a la base de datos.
