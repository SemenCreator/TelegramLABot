import logging
from aiogram import executor
import test_1
from test_2 import dp

logging.basicConfig(level=logging.INFO)


test_1.register_handlers_admin_1_level(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
