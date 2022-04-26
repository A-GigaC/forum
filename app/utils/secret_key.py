import os
from dotenv import load_dotenv

load_dotenv()

def secret_key():
    SECRET_KEY = str(os.getenv('SECRET_KEY'))
    return SECRET_KEY