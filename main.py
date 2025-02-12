import asyncio
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from App.handlers import router
import os

load_dotenv()  # Загружаем переменные из .env

API_TOKEN = os.getenv("API_TOKEN")  # Получаем токен из .env

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
