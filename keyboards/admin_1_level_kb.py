from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


bad_name = KeyboardButton('Имя')
bad_gender = KeyboardButton('Пол')
bad_description = KeyboardButton('Описание')
bad_photo = KeyboardButton('Фото')
bad_all = KeyboardButton('Нужно переделывать всю анкету')

reject_form_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True)

reject_form_kb.row(bad_name, bad_gender).row(
    bad_description, bad_photo).add(bad_all)
