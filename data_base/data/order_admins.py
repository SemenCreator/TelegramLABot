import sqlalchemy
from sqlalchemy import orm
from data_base.data.db_session import SqlAlchemyBase


class OrderAdmins(SqlAlchemyBase):
    __tablename__ = 'order_admins'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    form_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("forms.id"))
    state_now = sqlalchemy.Column(sqlalchemy.Boolean)
    state_check = sqlalchemy.Column(sqlalchemy.Boolean)

    form = orm.relation('Form')
