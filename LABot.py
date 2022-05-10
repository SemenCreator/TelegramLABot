from aiogram.utils import executor

from handlers import admin_1_level, student
from data_base.data import db_session

from create_bot import dp


async def on_startup(_):
    print('Бот вышел в онлайн')
    db_session.global_init('data_base//db//LABot.db')

student.register_handlers_client(dp)
admin_1_level.register_handlers_admin_1_level(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
