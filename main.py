from aiogram.types import Message
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from logging import basicConfig, DEBUG
from asyncio import run
from aiogram.enums import ParseMode
from requests import get

# Настройка логирования
basicConfig(level=DEBUG)

# Загрузка токена из .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY не задан в .env файле")

# Создаем бота, диспетчер и роутер
bot = Bot(token=API_KEY,)
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


@dp.message(Command('site_analysis'))
async def site_analysis(message: Message):
    from key_words import KEY_WORDS
    from status import status_by_code
    from parsing_sites import SITES
    for site_link, parse_handler in SITES.items():
        response = get(site_link)
        status_code = response.status_code
        response_for_user =  parse_handler()
        print(response_for_user)
        if response_for_user:
            await message.answer(response_for_user)
        #if status_code in status_by_code:
            #await message.answer(f"status: {status_code} - {status_by_code[status_code]}")
            #html_code = response.text
            #await message.answer(html_code[:4000])
        #else:
            #await message.answer(f'получен неизвестный код: {status_code}')
            #await message.answer(site_link)


# Обработчик команды /parse
@dp.message(Command("parse"))
async def parse_handler(message: Message):
    from requests import get
    from bs4 import BeautifulSoup
    from status import status_by_code
    message_text = message.text
    command,url = message_text.split()
    await message.answer(f'буду парсить {url}')
    # Отключаем проверку SSL-сертификатов
    response = get(url)
    status_code = response.status_code
    
    if status_code in status_by_code:
        await message.answer(f"status: {status_code} - {status_by_code[status_code]}")
        html_code = response.text
        await message.answer(html_code[:4000])
    else:
        await message.answer(f'получен неизвестный код: {status_code}')

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