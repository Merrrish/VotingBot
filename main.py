import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from App.handlers import router  # Импортируем роутеры из обработчиков

# Загружаем переменные из .env
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Основная функция для запуска бота
async def main():
    dp.include_router(router)  # Включаем роутер
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
