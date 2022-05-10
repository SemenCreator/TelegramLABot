from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data_base.data import db_session
from data_base.data.forms import Form
# from data_base.data.search import Searching
from data_base.data.order_admins import OrderAdmins
from data_base.data.first_checking_forms import FirstCheckingForm
from data_base.db_requests import record_and_change

from create_bot import bot


async def form_read(person_id, chat_id):
    db_sess = db_session.create_session()
    for form in db_sess.query(Form).filter(Form.person_id == person_id):
        await bot.send_photo(chat_id, form.photo, f'{form.name} {form.age} \
    \nОписание: {form.description}\n{form.subjects}')


async def person_in_form_id(person_id):
    db_sess = db_session.create_session()
    person = db_sess.query(Form).filter(Form.person_id == person_id).first()
    return person.id


async def check_message_id(message_id):
    db_sess = db_session.create_session()
    now_form = db_sess.query(FirstCheckingForm).filter(
        FirstCheckingForm.message_id == message_id).first()
    if now_form is None:
        return False
    else:
        return True


async def all_admins():
    db_sess = db_session.create_session()
    for admin in db_sess.query(Form).filter(Form.is_admin is True):
        new_admin = OrderAdmins()
        new_admin.form_id = admin.id
        new_admin.state_now = False
        new_admin.state_check = False
        db_sess.add(new_admin)
    db_sess.commit()


async def choose_admin():
    db_sess = db_session.create_session()
    next_admin = db_sess.query(OrderAdmins).filter(
        OrderAdmins.state_now is not True).first()
    if next_admin is None:
        await record_and_change.clear_work_admin()
    admin_id = await get_admin_person_id(next_admin.form_id)
    await record_and_change.change_state_now(next_admin)
    db_sess.commit()
    return admin_id


async def get_admin_person_id(form_id):
    db_sess = db_session.create_session()
    admin_id = db_sess.query(Form).filter(
        Form.id == form_id).first()
    db_sess.commit()
    return admin_id.person_id


async def send_admin(person_id, admin_id):
    db_sess = db_session.create_session()
    form = db_sess.query(Form).filter(Form.person_id == person_id).first()
    await bot.send_photo(admin_id, form.photo, f'{form.name} {form.age} \
                        \nОписание: {form.description}\n{form.subjects}',
                         reply_markup=InlineKeyboardMarkup().
                         add(InlineKeyboardButton(
                             'Принять', callback_data=f'yes{person_id}'),
                             InlineKeyboardButton(
                                 'Отклонить', callback_data=f'no{person_id}')))
    db_sess.commit()
