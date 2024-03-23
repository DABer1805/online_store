import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Item(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'items'
    # ID товара
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    # Название товара
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Цена товара
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # Скидка на товар
    discount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # ID поставщика
    supplier = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('suppliers.id'))
    # Какая категория у товара
    category = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('categories.id'))
    # Категории товаров
    categories = orm.relationship('Category')
    # Поставщики
    suppliers = orm.relationship('Supplier')
