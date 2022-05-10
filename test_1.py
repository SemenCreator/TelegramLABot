from aiogram import types, Dispatcher
import datetime
import aioschedule as schedule
import asyncio
import time


async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


async def job_that_executes_once():
    await f(types.Message)


async def f(message: types.Message):
    await message.answer('Мечта')


period = datetime.datetime.today()
period += datetime.timedelta(minutes=1)
period = period.strftime('%H:%M')
schedule.every().day.at(period).do(job_that_executes_once)
loop = asyncio.get_event_loop()


def register_handlers_admin_1_level(dp: Dispatcher):
    dp.register_message_handler(
        process_start_command, commands=['start'])


while True:
    print('9')
    loop.run_until_complete(schedule.run_pending())
    time.sleep(1)
