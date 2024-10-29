from pydantic import BaseModel

class ChatbotSetting(BaseModel):
    welcomeMessage : str
    position : str
    primaryColor : str
    secondaryColor: str
    thirdColor: str
    fontSize : str

class Chatbot(BaseModel):
    _id : str
    clientId : str
    name : str
    active : bool
    setting: ChatbotSetting

class Message(BaseModel):
    text : str