from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import string

from keyboards import student_kb
from data_base.db_requests import record_and_change, get_and_send
from handlers import admin_1_level


like_subjects = []
russian_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
available_symbols = list(string.ascii_letters) + list(string.punctuation) + \
    list(russian_alphabet) + list(russian_alphabet.upper())


class CreateForm(StatesGroup):
    name = State()
    age = State()
    gender = State()
    description = State()
    photo = State()
    subjects = State()


class CreateSearch(StatesGroup):
    gender_search = State()
    start_age_search = State()
    end_age_search = State()


class EditForm(StatesGroup):
    edit_photo = State()
    edit_description = State()
    edit_subjects = State()


async def choose_subject(subject):
    global like_subjects
    if subject != '+':
        if subject == student_kb.subjects[0] or \
                subject == student_kb.subjects[-1]:
            like_subjects = [subject]
            return False
        else:
            return True
    else:
        return False


def check_age(age):
    if type(age) == int:
        if age > 6 and age < 19:
            return True
        else:
            return False
    else:
        return False


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК', reply_markup=student_kb.main_kb)


async def start_bot(message: types.Message):
    await message.reply('Привет! Я школьный бот для знакомств в Telegram. \
Нажмите продолжить, чтобы создать свою анкету и начать поиск',
                        reply_markup=student_kb.start_kb)


async def before_form(message: types.Message):
    await CreateForm.name.set()
    await message.answer('Введи своё настоящее имя',
                         reply_markup=types.ReplyKeyboardRemove())


async def input_name(message: types.Message, state: FSMContext):
    global available_symbols
    name = message.text
    name_symbols = set(name)
    print(len(name_symbols), name_symbols, set(available_symbols))
    if len(name_symbols.intersection(set(available_symbols))) \
            == len(name_symbols):
        async with state.proxy() as data:
            data['person_id'] = message.from_user.id
            data['name'] = message.text
        await CreateForm.next()
        await message.answer("Введи свой возраст")
    else:
        await message.reply('Пожалуйста введите имя используя только символы \
строки и пунктуации')


async def input_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            age = int(message.text)
        except ValueError:
            await message.reply('Пожалуйста введите возраст целочисленным \
числом')
            return
        if check_age(age):
            data['age'] = age
            await CreateForm.next()
            await message.answer('Выберите свой пол',
                                 reply_markup=student_kb.choose_gender)
        else:
            await message.reply('Пожалуйста введите свой настоящий возраст')


async def input_gender(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender == 'мужской' or gender == 'женский':
        async with state.proxy() as data:
            data['gender'] = message.text
        await CreateForm.next()
        await message.answer("Теперь введи описание. Для лучшей совместимости, \
укажите любимый спорт, фильм, компьютерную игру и т.д.",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply('Пожалуйста, выберите свой пол')


async def input_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await CreateForm.next()
    await message.answer("Загрузите своё фото, обязательно отметьте галочкой \
пункт Compress images.")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == 'photo':
            data['photo'] = message.photo[0].file_id
            await CreateForm.next()
            await message.answer("Выбери любимые предметы. Напиши + в чат когда \
окончишь выбор",
                                 reply_markup=student_kb.favourite_subjects)
        else:
            await message.reply('Пожалуйста отправьте боту ваше фото, а не сообщение \
или файл')


async def choose_favourite_subjects(message: types.Message, state: FSMContext):
    global like_subjects
    subject = message.text
    input_subject = await choose_subject(subject)
    if input_subject:
        if subject in student_kb.subjects:
            like_subjects.append(subject)
        like_subjects = list(set(like_subjects))
    else:
        async with state.proxy() as data:
            data['subjects'] = like_subjects
        await message.answer(data)
        await record_and_change.add_form(state)
        person_id = message.from_user.id
        await get_and_send.form_read(person_id, message.chat.id)
        await message.answer('Если вас все устраивает в анкете \
нажмите Меня все устраивает, если вы хотите её измененить, выберите Заполнить\
 анкету заново.',
                             reply_markup=student_kb.start_search_kb)
        like_subjects = []
        await state.finish()


async def start_search(message: types.Message):
    await CreateSearch.gender_search.set()
    await message.answer('Выберите пол человека для поиска',
                         reply_markup=student_kb.choose_gender)


async def need_gender(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender == 'мужской' or gender == 'женский':
        async with state.proxy() as data:
            data['gender'] = message.text
        await CreateSearch.next()
        await message.answer("Теперь введи возраст, с которого \
будем вести поиск", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply('Пожалуйста, выберите свой пол')


async def start_age(message: types.Message, state: FSMContext):
    try:
        start_age = int(message.text)
    except ValueError:
        await message.reply('Пожалуйста введите возраст целочисленным \
числом')
        return
    async with state.proxy() as data:
        if check_age(start_age):
            data['start_age'] = start_age
            await CreateSearch.next()
            await message.answer("Теперь введи возраст, до которого \
будем вести поиск")
        else:
            await message.reply('Пожалуйста, введи реальный возраст, с которого \
будем вести поиск')


async def end_age(message: types.Message, state: FSMContext):
    try:
        end_age = int(message.text)
    except ValueError:
        await message.reply('Пожалуйста введите возраст целочисленным \
числом')
        return
    async with state.proxy() as data:
        if check_age(end_age):
            if end_age >= data['start_age']:
                data['end_age'] = end_age
                await message.answer(data)
                await message.answer('Поздравляем! Вы прошли регистрацию! \
Ваша анкета отправлена на модерацию и, как только она пройдёт проверку \
вы получите ответ')
                await state.finish()
                person_id = message.from_user.id
                print(person_id)
                await admin_1_level.number_admin(person_id)
            else:
                await message.reply("Пожалуйста, введи возраст, до которого \
будем вести поиск, так чтобы он был меньше или равен возраст с которого будем \
вести поиск")
        else:
            await message.reply("Пожалуйста, введи реальный возраст, до которого \
будем вести поиск")


async def edit_form(message: types.Message):
    await get_and_send.form_read(message.from_user.id, message.chat.id)
    await message.answer('Выберите, что хотите поменять в анкете. \
Напишите назад, если хотите вернуться назад',
                         reply_markup=student_kb.edit_form_kb)


async def middle_edit_photo(message: types.Message):
    await message.reply("Загрузите своё фото, обязательно отметьте галочкой \
пункт Compress images.", reply_markup=types.ReplyKeyboardMarkup())
    await EditForm.edit_photo.set()


async def edit_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        await record_and_change.change_photo(message.from_user.id,
                                             message.photo[0].file_id)
        await message.answer('Фото успешно изменено',
                             reply_markup=student_kb.main_kb)
        await state.finish()
    else:
        if message.text == 'назад':
            await message.answer('Вы успешно вернулись назад',
                                 reply_markup=student_kb.edit_form_kb)
            await state.finish()
        else:
            await message.reply('Пожалуйста отправьте боту ваше фото, а не сообщение \
или файл')


async def middle_edit_description(message: types.Message):
    await message.reply("Напишите новое описание",
                        reply_markup=types.ReplyKeyboardMarkup())
    await EditForm.edit_description.set()


async def edit_description(message: types.Message, state: FSMContext):
    if message.text == 'назад':
        await message.answer('Вы успешно вернулись назад',
                             reply_markup=student_kb.edit_form_kb)
        await state.finish()
    else:
        await record_and_change.change_description(message.from_user.id,
                                                   message.text)
        await message.answer('Описание успешно изменено',
                             reply_markup=student_kb.main_kb)
        await state.finish()


async def middle_edit_subjects(message: types.Message):
    await message.reply("Выбери любимые предметы. Напиши + в чат когда \
окончишь выбор", reply_markup=student_kb.favourite_subjects)
    await EditForm.edit_subjects.set()


async def edit_subjects(message: types.Message, state: FSMContext):
    global like_subjects
    subject = message.text
    input_subject = await choose_subject(subject)
    if input_subject:
        if subject in student_kb.subjects:
            like_subjects.append(subject)
        else:
            if subject == 'назад':
                await message.answer('Вы успешно вернулись назад',
                                     reply_markup=student_kb.edit_form_kb)
                await state.finish()
        like_subjects = list(set(like_subjects))
    else:
        await record_and_change.change_subjects(message.from_user.id,
                                                like_subjects)
        await message.answer('Список любимых предметов успешно изменен',
                             reply_markup=student_kb.main_kb)
        like_subjects = []
        await state.finish()


async def back_to_menu(message: types.Message):
    await message.answer('Вы вернулись в главное меню',
                         reply_markup=student_kb.main_kb)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(cancel_handler, Text(
        equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(before_form, Text(
        equals='продолжить', ignore_case=True))
    dp.register_message_handler(before_form, Text(
        equals='Заполнить анкету заново', ignore_case=True))
    dp.register_message_handler(input_name, state=CreateForm.name)
    dp.register_message_handler(input_age, state=CreateForm.age)
    dp.register_message_handler(input_gender, state=CreateForm.gender)
    dp.register_message_handler(
        input_description, state=CreateForm.description)
    dp.register_message_handler(
        load_photo, content_types=['photo', 'text', 'document'],
        state=CreateForm.photo)
    dp.register_message_handler(choose_favourite_subjects,
                                state=CreateForm.subjects)
    dp.register_message_handler(start_search, Text(
        equals='Меня все устраивает', ignore_case=True))
    dp.register_message_handler(need_gender, state=CreateSearch.gender_search)
    dp.register_message_handler(start_age, state=CreateSearch.start_age_search)
    dp.register_message_handler(end_age, state=CreateSearch.end_age_search)
    dp.register_message_handler(start_search, commands=['edit_search'])
    dp.register_message_handler(start_search, Text(
        equals='Редактировать поиск', ignore_case=True))
    dp.register_message_handler(edit_form, commands=['edit_form'])
    dp.register_message_handler(edit_form, Text(
        equals='Редактировать анкету', ignore_case=True))
    dp.register_message_handler(middle_edit_photo, Text(
        equals='Редактировать фото', ignore_case=True))
    dp.register_message_handler(edit_photo, state=EditForm.edit_photo,
                                content_types=['photo', 'text', 'document'])
    dp.register_message_handler(middle_edit_description, Text(
        equals='Редактировать описание', ignore_case=True))
    dp.register_message_handler(edit_description,
                                state=EditForm.edit_description)
    dp.register_message_handler(middle_edit_subjects, Text(
        equals='Выбрать любимые предметы', ignore_case=True))
    dp.register_message_handler(edit_subjects,
                                state=EditForm.edit_subjects)
    dp.register_message_handler(back_to_menu, Text(
        equals='Главное меню', ignore_case=True))
