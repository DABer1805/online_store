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
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    # Скидка на товар
    discount = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    # ID поставщика
    supplier = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('suppliers.id'))
    # Какая категория у товара
    category = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('categories.id'))
    # Бренд товара
    brand = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Вид продукта
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Тип упаковки
    type_of_packing = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Ширина, см
    width = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Высота, см
    height = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Глубина, см
    depth = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Вес, кг
    weight = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Eмкость, л
    capacity = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Минимальная температура хранения
    min_temp = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Максимальная температура хранения
    max_temp = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Срок годности
    expiration_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Калории
    calories = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Белки
    squirrels = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Жиры
    fats = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Углеводы
    carbohydrates = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Описание товара
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Состав товара
    composition = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Категории товаров
    categories = orm.relationship('Category')
    # Поставщики
    suppliers = orm.relationship('Supplier')
