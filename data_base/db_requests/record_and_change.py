from data_base.data import db_session
from data_base.data.forms import Form
# from data_base.data.search import Searching
from data_base.data.order_admins import OrderAdmins
from data_base.data.first_checking_forms import FirstCheckingForm
from data_base.db_requests import get_and_send


async def add_components(user, form_items, person_id):
    user.person_id = person_id
    user.name = form_items[1]
    user.age = form_items[2]
    user.gender = form_items[3]
    user.description = form_items[4]
    user.photo = form_items[5]
    user.subjects = f"Любимые предметы: {', '.join(form_items[6])}"
    user.checking = 0
    user.is_admin = True


async def add_form(state):
    async with state.proxy() as data:
        form_items = tuple(data.values())
        db_sess = db_session.create_session()
        id = form_items[0]
        amount = db_sess.query(Form).filter(Form.person_id == id).count()
        person = db_sess.query(Form).filter(Form.person_id == id).first()
        if amount > 0:
            await add_components(person, form_items, id)
        else:
            form = Form()
            await add_components(form, form_items, id)
            db_sess.add(form)
        db_sess.commit()


async def change_checking(id, result):
    db_sess = db_session.create_session()
    person = db_sess.query(Form).filter(Form.person_id == id).first()
    if result:
        person.checking = 1
    else:
        person.checking = 0


async def record_first_checking(admin_1_id, person_id, result,
                                reason_refuse, description_reason):
    db_sess = db_session.create_session()
    first_checking_form = FirstCheckingForm()
    first_checking_form.admin_1_id = admin_1_id
    first_checking_form.form_id = \
        await get_and_send.person_in_form_id(person_id)
    first_checking_form.result = result
    first_checking_form.reason_refuse = reason_refuse
    first_checking_form.description_reason = description_reason
    db_sess.add(first_checking_form)
    db_sess.commit()


async def change_photo(person_id, photo):
    db_sess = db_session.create_session()
    person = db_sess.query(Form).filter(Form.person_id == person_id).first()
    person.photo = photo
    db_sess.commit()


async def change_description(person_id, description):
    db_sess = db_session.create_session()
    person = db_sess.query(Form).filter(Form.person_id == person_id).first()
    person.description = description
    db_sess.commit()


async def change_subjects(person_id, like_subjects):
    db_sess = db_session.create_session()
    person = db_sess.query(Form).filter(Form.person_id == person_id).first()
    person.subjects = f"Любимые предметы: {' '.join(like_subjects)}"
    db_sess.commit()


async def clear_work_admin():
    db_sess = db_session.create_session()
    for new_admin in db_sess.query(OrderAdmins):
        new_admin.state_now = False
        new_admin.state_check = False
    db_sess.commit()


async def change_state_check(admin_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Form).filter(
        Form.person_id == admin_id).first()
    admin = db_sess.query(OrderAdmins).filter(
        OrderAdmins.form_id == user.id).first()
    admin.state_check = True
    db_sess.commit()


async def change_state_now(next_admin):
    next_admin.state_now = True
