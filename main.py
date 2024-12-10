from aiogram import Bot,Dispatcher
API_KEY = '7043185547:AAGBVS_Z0LoAKQY8EshimvjGcTXmP-rh-UU'

patcher_bot = Bot(API_KEY) #это бот, он умеет все что угодно, но не принимает запросы
router = Dispatcher() #это диспатчер он не умеет ничего, но смотрит кто что делвет (управляющий)
