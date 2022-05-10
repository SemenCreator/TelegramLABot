from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


bot = Bot(token="5384464842:AAFYLJaJJyvDCd1jY_JPT1QDEQlGwaeQmDE")
dp = Dispatcher(bot, storage=storage)
