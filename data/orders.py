import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'
    # ID заказа
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    # Список товаров в формате "<id>x<кол-во товаров>,<id>x<кол-во
    # товаров>,...<id>x<кол-во товаров>"
    items_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Дата создание заказа
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    # Дата закрытия заказа
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    # Закрыт ли заказ
    is_complited = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    # ID пользователя, который сделал заказ
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    # Пользователь, который сделал заказ
    user = orm.relationship('User')