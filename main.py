from dotenv import load_dotenv
from logging import basicConfig, DEBUG
import os
from asyncio import run
from aiogram import Bot,Dispatcher

load_dotenv() #выгружаем переменные из env файла
API_KEY = os.getenv('API_KEY')
patcher_bot = Bot(API_KEY) #это бот, он умеет все что угодно, но не принимает запросы
router = Dispatcher() #это диспатчер он не умеет ничего, но смотрит кто что делвет (управляющий)
basicConfig(level = DEBUG) #включили логирование

async def main():
    try:
        router.start_polling(patcher_bot)
        await patcher_bot.delete_webhook(drop_pending_updates=True)
    except Exception as E:
        print(E)

if __name__ == "__main__":
    run(main())