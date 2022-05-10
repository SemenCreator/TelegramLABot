import sqlalchemy
from sqlalchemy import orm
from data_base.data.db_session import SqlAlchemyBase


class Searching(SqlAlchemyBase):
    __tablename__ = 'search'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    form_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("forms.id"))
    gender_search = sqlalchemy.Column(sqlalchemy.String)
    start_age_search = sqlalchemy.Column(sqlalchemy.Integer)
    end_age_search = sqlalchemy.Column(sqlalchemy.Integer)

    form = orm.relation('Form')
