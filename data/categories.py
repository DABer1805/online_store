import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'
    # ID категории
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    # Название категории
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Товары
    items = orm.relationship('Item', back_populates='categories')
