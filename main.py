from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from app.users.routes.user_routes import router as user_routes
from app.chatbots.routes.chatbot_routes import router as chatbot_routes
#from app.sessions.routes.sessions_routes import router as sessions_routes
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.firebase.firebase_service import initialice_firebase
from fastapi.templating import Jinja2Templates
from fastapi.templating import Jinja2Templates

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
templates = Jinja2Templates(directory="app/templates")

@app.get("/chatbot", response_class=HTMLResponse)
async def get_chatbot(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(chatbot_routes)
app.include_router(user_routes)
#app.include_router(sessions_routes)

#Crear un endpoint de salud (/health o /status) para verificar el funcionamiento de la API y del acceso a la base de datos.
