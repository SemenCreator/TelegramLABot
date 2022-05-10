import sqlalchemy
from sqlalchemy import orm
from data_base.data.db_session import SqlAlchemyBase


class Form(SqlAlchemyBase):
    __tablename__ = 'forms'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    person_id = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    gender = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    photo = sqlalchemy.Column(sqlalchemy.String)
    subjects = sqlalchemy.Column(sqlalchemy.String)
    checking = sqlalchemy.Column(sqlalchemy.Boolean)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean)

    seacrh = orm.relation("Searching", back_populates='form')
    first_checking_form = orm.relation(
        "FirstCheckingForm", back_populates='form')
    seacrh = orm.relation("OrderAdmins", back_populates='form')
