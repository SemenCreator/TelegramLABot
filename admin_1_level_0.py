from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.admin_1_level_kb import reject_form_kb
from data_base.db_requests.record_and_change import change_checking, record_first_checking
from data_base.db_requests.record_and_change import record_in_middle_form, get_middle_id
from data_base.db_requests.record_and_change import check_form_now, check_message_id
from data_base.db_requests.record_and_change import get_message_id
from aiogram.dispatcher.filters import Text
from keyboards.student_kb import start_kb, main_kb


class ExplanationRefusal(StatesGroup):
    reason = State()
    add_message = State()
    confirmation = State()


async def check_verify_now():
    result = await check_form_now()
    return result


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await record_in_middle_form('', '', False)
    await state.finish()
    await message.reply('ОК')


async def accept_form(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    if await check_verify_now():
        await callback_query.answer('В время процесса принятия одной анкеты, \
зарегистроровать другую невозможно. Подождите немного...')
    elif await check_message_id(message_id):
        await callback_query.answer('Данная анкета уже обработана')
    else:
        person_id = callback_query.data.replace("yes", "")
        await record_in_middle_form(person_id, message_id, True)
        await callback_query.answer('Напишите принять, если хотите продолжить')


async def confirmation_form(message: types.Message):
    person_id = await get_middle_id()
    message_id = await get_message_id()
    await record_in_middle_form('', '', False)
    await change_checking(person_id, 'accept')
    await record_first_checking(message.from_user.id, person_id, True,
                                message_id, '', '')
    await bot.send_message(person_id, 'Поздравляем ваша анкета \
    зарегистрирована теперь вам доступны все функции бота. Нажмите начать \
поиск чтобы смотреть анкеты', reply_markup=main_kb)


async def reject_form(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    if await check_verify_now():
        await callback_query.answer('В время процесса принятия одной анкеты, \
зарегистроровать другую невозможно. Подождите немного...')
    elif await check_message_id(message_id):
        await callback_query.answer('Данная анкета уже обработана')
    else:
        person_id = callback_query.data.replace("no", "")
        await record_in_middle_form(person_id, message_id, True)
        await callback_query.answer('Напишите отклонить, если хотите \
продолжить.')


async def start_description_problem_form(message: types.Message):
    await message.answer('Пожалуйста выберите причину, по которой отклоняйте анкету. \
Если вы хотите отменить действие напишите отмена боту.',
                         reply_markup=reject_form_kb)
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
    async with state.proxy() as data:
        if message.text == '-':
            data['plus_message'] = 'Причина отказа не сопровождается \
сообщением'
        else:
            data['plus_message'] = message.text
    person_id = await get_middle_id()
    await bot.send_message(person_id, f"К сожалению ваша анкета \
не прошла регистрацию. Причина: {data['reason']}")
    await bot.send_message(person_id, "Пожалуйста заполните свою анкету \
заново", reply_markup=start_kb)
    await bot.send_message(person_id, data['plus_message'])
    await change_checking(person_id, 'reject')
    message_id = await get_message_id()
    await record_first_checking(message.from_user.id, person_id, False,
                                message_id, data['reason'],
                                data['plus_message'])
    await record_in_middle_form('', '', False)
    await state.finish()


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
