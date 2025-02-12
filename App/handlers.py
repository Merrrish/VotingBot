import asyncio
import logging
from aiogram import Bot, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, PollAnswer
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла
load_dotenv()

# Получаем токены из .env
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
router = Router()

router.message.filter(F.chat.type == "supergroup", F.from_user.id == 6568586074)  # Фильтрация только для нужного пользователя и супергруппы

poll_results = {}  # Хранилище результатов голосов

class Vote(StatesGroup):
    nname = State()  # Состояние для хранения никнейма пользователя

@router.message(Command('vote'))
async def vote(message: Message, state: FSMContext):
    if not message.reply_to_message:
        await message.answer("Пожалуйста, используйте команду /vote в ответ на сообщение пользователя, которого хотите исключить.")
        return

    user_to_vote = message.reply_to_message.from_user

    # Сохранение данных о пользователе, которого хотят исключить
    await state.update_data(user_id=user_to_vote.id, nname=user_to_vote.username)
    data = await state.get_data()

    poll_message = await bot.send_poll(
        chat_id=message.chat.id,
        question=f'Хотите ли вы исключить пользователя {data["nname"]}?',
        options=['Да', 'Нет'],
        is_anonymous=False,
        allows_multiple_answers=False
    )

    poll_results[poll_message.poll.id] = {"Да": 0, "Нет": 0}
    print(f"Инициализация результатов для опроса {poll_message.poll.id}: {poll_results[poll_message.poll.id]}")

    await asyncio.sleep(5)
    await state.clear()  # Очищаем состояние

    await bot.stop_poll(
        chat_id=poll_message.chat.id,
        message_id=poll_message.message_id
    )

    results = poll_results.pop(poll_message.poll.id)
    yes_votes = results["Да"]
    no_votes = results["Нет"]

    await message.answer(f"Результаты опроса:\nДа: {yes_votes}\nНет: {no_votes}")

    if yes_votes > no_votes:
        await message.answer(f"Пользователь {data['nname']} будет исключен.")
        try:
            await bot.ban_chat_member(chat_id=message.chat.id, user_id=data["user_id"])
            await message.answer(f"Пользователь {data['nname']} был исключен.")
        except Exception as e:
            await message.answer(f"Не удалось исключить пользователя {data['nname']}. Ошибка: {e}")
    else:
        await message.answer(f"Пользователь {data['nname']} не будет исключен.")

@router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    poll_id = poll_answer.poll_id
    option_ids = poll_answer.option_ids

    # Обновление результатов голосования
    if poll_id in poll_results:
        if 0 in option_ids:
            poll_results[poll_id]["Да"] += 1
        if 1 in option_ids:
            poll_results[poll_id]["Нет"] += 1

    print(f"Голос получен: {poll_results}")
