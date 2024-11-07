import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

load_dotenv()
def initialice_firebase():
    cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS_PATH"))
    firebase_admin.initialize_app(cred)