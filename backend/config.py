import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL') 
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
YANDEX_API = os.getenv('YANDEX_API')