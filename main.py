from aiogram.types import Message
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from logging import basicConfig, DEBUG
from asyncio import run
import aiohttp
from bs4 import BeautifulSoup
from aiogram.enums import ParseMode

# Настройка логирования
basicConfig(level=DEBUG)

# Загрузка токена из .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY не задан в .env файле")

# Создаем бота, диспетчер и роутер
bot = Bot(token=API_KEY, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()

# Обработчик команды /hi
@router.message(Command("hi"))
async def say_hi(message: Message):
    await message.answer("Привет!")

@router.message(Command("start"))
async def start_function(message: Message):
    await message.answer('''Здравсвуйте, я Parser-bot!
Мои основные команды:
/find - начинаю поиск
''')

@router.message(Command('ID'))
async def get_id(message: Message):
    user_id = message.from_user.id
    await message.answer(f'вот ваш id {user_id}')

async def say_me_hello():
    my_id = 5453726012
    await bot.send_message(my_id,'hi')
    
async def repeat_infinity():
    while True:
        await say_me_hello()

async def fetch_data():
    url = "https://quotes.toscrape.com/"  # Пример сайта с цитатами
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            quotes = soup.find_all("span", class_="text")
            return [quote.text for quote in quotes[:5]]  # Берем первые 5 цитат

# Обработчик команды /parse
@dp.message(Command("parse"))
async def parse_handler(message: Message):
    quotes = await fetch_data()
    response_text = "\n\n".join(quotes)
    await message.answer(f"Вот несколько цитат:\n\n{response_text}")

# Основная функция
async def main():
    # Удаляем вебхук перед запуском polling
    await bot.delete_webhook(drop_pending_updates=True)

    # Подключаем роутеры
    dp.include_router(router)
   # await repeat_infinity()


    # Запуск polling
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    run(main())