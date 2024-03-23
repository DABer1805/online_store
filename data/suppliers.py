import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Supplier(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'suppliers'

    # ID поставщика
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    # Название поставщика
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Расчетный счет
    payment_account = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Адрес поставщика
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Мобильный телефон пользователя
    mobile_phone = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=True
    )
    # Электронная почта поставщика
    email = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=True
    )
    # Товары
    items = orm.relationship('Item', back_populates='suppliers')
