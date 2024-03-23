import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    # ID пользователя
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    # Фамилия пользователя
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Имя пользователя
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Список товаров в формате "<id>x<кол-во товаров>,<id>x<кол-во
    # товаров>,...<id>x<кол-во товаров>" (корзина пользователя)
    items_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Мобильный телефон пользователя
    mobile_phone = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=True
    )
    # Хэшированный пароль пользователя
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Заказы пользователя
    orders = orm.relationship('Order', back_populates='user')

    def set_password(self, password):
        """ Записываем хэшированный пароль """
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """ Проверка пароля """
        return check_password_hash(self.hashed_password, password)
