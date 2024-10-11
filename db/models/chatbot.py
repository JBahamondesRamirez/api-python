from pydantic import BaseModel

class Config(BaseModel):
    _id : str
    clientId : str
    welcomeMessage : str
    errorMessage: str
    position : str
    primaryColor : str
    secondaryColor: str
    thirdColor: str
    font : str
    fontSize : str
    urlAvatar: str

class Message(BaseModel):
    text : str

