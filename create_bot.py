from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='5384464842:AAFYLJaJJyvDCd1jY_JPT1QDEQlGwaeQmDE')
dp = Dispatcher(bot, storage=storage)
