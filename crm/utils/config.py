from dotenv import load_dotenv
import os

load_dotenv()  # Загружает .env в переменные окружения

MANAGER_USERNAME = os.getenv("MANAGER_USERNAME")
MANAGER_PASSWORD = os.getenv("MANAGER_PASSWORD")
SUBSCRIBER_PHONE = os.getenv("SUBSCRIBER_PHONE")
