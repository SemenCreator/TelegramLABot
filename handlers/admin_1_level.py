from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from data_base.db_requests import record_and_change, get_and_send
from keyboards import student_kb, admin_1_level_kb

from create_bot import bot


person_id = ''


class ExplanationRefusal(StatesGroup):
    reason = State()
    add_message = State()


async def number_admin(user_id, **kwargs):
    admin_id = await get_and_send.choose_admin()
    await get_and_send.send_admin(user_id, admin_id)


async def change_check():
    pass


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


async def accept_form(callback_query: types.CallbackQuery):
    global person_id
    person_id = callback_query.data.replace("yes", "")
    await callback_query.answer('Напишите принять, если хотите продолжить')
    print(person_id)


async def confirmation_form(message: types.Message):
    global person_id
    await record_and_change.change_checking(person_id, 'accept')
    print(person_id, message.from_user.id)
    await record_and_change.record_first_checking(message.from_user.id,
                                                  person_id, True, '', '')
    await bot.send_message(person_id, 'Поздравляем ваша анкета \
    зарегистрирована теперь вам доступны все функции бота. Нажмите начать \
поиск чтобы смотреть анкеты', reply_markup=student_kb.main_kb)
    # await db_requests.change_state_check(message.from_user.id)
    person_id = ''


async def reject_form(callback_query: types.CallbackQuery):
    global person_id
    person_id = callback_query.data.replace("no", "")
    await callback_query.answer('Напишите отклонить, если хотите продолжить')


async def start_description_problem_form(message: types.Message):
    await message.answer('Пожалуйста выберите причину, по которой отклоняйте анкету. \
Если вы хотите отменить действие напишите отмена боту.',
                         reply_markup=admin_1_level_kb.reject_form_kb)
    await ExplanationRefusal.reason.set()


async def reason(message: types.Message, state: FSMContext):
    reasons = 'Имя,Пол,Описание,Фото,Нужно переделывать всю анкету'.split(',')
    if message.text in reasons:
        async with state.proxy() as data:
            data['reason'] = message.text
            await message.answer('Добавьте сообщение с текстом о том, именно вам не нравится. \
Если вы не хотите ничего писать введите -')
            await ExplanationRefusal.next()
    else:
        await message.reply('Пожалуйста, выберите один из компонентов таблицы')


async def add_message(message: types.Message, state: FSMContext):
    global person_id
    async with state.proxy() as data:
        if message.text == '-':
            data['plus_message'] = 'Причина отказа не сопровождается \
сообщением'
        else:
            data['plus_message'] = message.text
    await bot.send_message(person_id, f"К сожалению ваша анкета \
не прошла регистрацию. Причина: {data['reason']}")
    await bot.send_message(person_id, "Пожалуйста заполните свою анкету \
заново", reply_markup=student_kb.start_kb)
    await bot.send_message(person_id, data['plus_message'])
    await record_and_change.change_checking(person_id, False)
    await record_and_change.record_first_checking(message.from_user.id,
                                                  person_id, False,
                                                  data['reason'],
                                                  data['plus_message'])
    await state.finish()
    person_id = ''


def register_handlers_admin_1_level(dp: Dispatcher):
    dp.register_message_handler(start_description_problem_form, Text(
        equals='отклонить', ignore_case=True))
    dp.register_message_handler(
        reason, state=ExplanationRefusal.reason)
    dp.register_message_handler(
        add_message, state=ExplanationRefusal.add_message)
    dp.register_callback_query_handler(
        accept_form, lambda x: x.data and x.data.startswith('yes'), state='*')
    dp.register_message_handler(confirmation_form, Text(
        equals='принять', ignore_case=True))
    dp.register_callback_query_handler(
        reject_form, lambda x: x.data and x.data.startswith('no'), state='*')
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(
        equals='отмена', ignore_case=True), state="*")
