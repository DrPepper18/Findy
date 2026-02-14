import os


def is_local_development():
    return not os.path.exists('/.dockerenv')


if is_local_development():
    from dotenv import load_dotenv
    load_dotenv()


ENVIRONMENT = os.getenv('ENVIRONMENT')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_NAME_TEST = os.getenv('DB_NAME_TEST')


def is_dev():
    return ENVIRONMENT == "dev"


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME_TEST}"