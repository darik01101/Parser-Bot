import aiohttp
import asyncio
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

TOKEN = "YOUR_BOT_TOKEN"  # Вставьте ваш токен

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Функция для парсинга данных
async def fetch_data():
    url = r"ya.ru"  # Пример сайта с цитатами
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            quotes = soup.find_all("span", class_="text")
            return [quote.text for quote in quotes[:5]]  # Берем первые 5 цитат

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Напиши /parse, чтобы получить данные.")

# Обработчик команды /parse
@dp.message(Command("parse"))
async def parse_handler(message: Message):
    quotes = await fetch_data()
    response_text = "\n\n".join(quotes)
    await message.answer(f"Вот несколько цитат:\n\n{response_text}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__== "__main__":
    asyncio.run(main())