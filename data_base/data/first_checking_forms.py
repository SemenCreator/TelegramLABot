import sqlalchemy
from sqlalchemy import orm

import datetime

from data_base.data.db_session import SqlAlchemyBase


class FirstCheckingForm(SqlAlchemyBase):
    __tablename__ = 'first_checking_forms'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    admin_1_id = sqlalchemy.Column(sqlalchemy.String)
    form_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("forms.id"))
    result = sqlalchemy.Column(sqlalchemy.Boolean)
    reason_refuse = sqlalchemy.Column(sqlalchemy.String)
    description_reason = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    form = orm.relation('Form')
