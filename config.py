import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET", "clave_secreta_dev")
    DB_HOST     = os.getenv("DB_HOST", "localhost")
    DB_NAME     = os.getenv("DB_NAME", "campusdb")
    DB_USER     = os.getenv("DB_USER", "campus_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_PORT     = os.getenv("DB_PORT", "5432")
