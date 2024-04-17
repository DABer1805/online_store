import os

from flask import jsonify
from flask_restful import Resource, abort, reqparse, request

from data import db_session
from data.constants import MAX_PRICE
from data.items import Item


class ItemsResource(Resource):
    def get(self, item_id):
        """ Получение товара по Id """
        # Проверяем есть ли товар в БД
        abort_if_item_not_found(item_id)
        # Сессия подключения к БД
        session = db_session.create_session()
        # Получаем товар по Id
        item = session.query(Item).get(item_id)
        # Инфа о товаре
        data = {
            'item': item.to_dict(only=(
                'id', 'name', 'price', 'discount',
                'category', 'brand', 'type', 'type_of_packing',
                'width', 'height', 'depth', 'weight',
                'capacity', 'min_temp', 'max_temp',
                'expiration_date', 'calories', 'squirrels',
                'fats', 'carbohydrates', 'description', 'composition'
            ))
        }
        # Добавляем поставщика
        data['item']['supplier'] = item.suppliers.name
        # Возвращаем инфу о товаре
        return jsonify(data)

    def delete(self, item_id):
        """ Получение товара по Id """
        # Проверяем есть ли товар в БД
        abort_if_item_not_found(item_id)
        # Сессия подключения к БД
        session = db_session.create_session()
        # Получаем товар по Id
        item = session.query(Item).get(item_id)
        # Удаляем товар из БД
        session.delete(item)
        # Удаляем фотку этого товара
        os.remove(f'static/img/items/item{item_id}.png')
        # Коммитим
        session.commit()
        session.close()
        # Возвращаем код успешной отправки
        return jsonify({'success': 'OK'})


class ItemsListResource(Resource):
    def get(self):
        """ Получение списка всех товаров, которые имеются """
        # Фильтры-категории
        categories = request.args.get('cat')
        # Фильтр максимальной цены
        max_price = request.args.get('max_price')
        # Фильтр - товары, только по скидке
        only_discount = request.args.get('only_discount')
        if max_price is None:
            # Если фильтр цены не указан, то устанавливаем
            # максимально возможную
            max_price = MAX_PRICE
        else:
            # Берем фильтр из аргументов
            max_price = float(max_price)

        # Сессия подключения к БД
        session = db_session.create_session()
        if only_discount:
            # Если только товары со скидкой
            items = session.query(Item).filter(Item.discount > 0)
        elif categories:
            # Если есть фильтры категорий
            categories = list(map(int, categories.split(',')))
            items = session.query(Item).filter(
                Item.category.in_(categories),
                Item.price * (1 - Item.discount * 0.01) <= max_price
            )
        else:
            # Все товары + фильтр цены
            items = session.query(Item).filter(
                Item.price * (1 - Item.discount * 0.01) <= max_price
            )
        session.close()
        # Возвращаем инфу о товарах
        return jsonify({
            'items': [
                item.to_dict(only=('id', 'name', 'price', 'discount'))
                for item in items
            ]})

    def post(self):
        """ Добавление товара """
        # Аргументы парсера
        args = parser.parse_args()
        # Сессия подключения к БД
        session = db_session.create_session()
        # Создаем обьект товара
        item = Item(
            name=args['name'],
            price=args['price'],
            discount=args['discount'],
            supplier=args['supplier'],
            category=args['category'],
            brand=args['brand'],
            type=args['type'],
            type_of_packing=args['type_of_packing'],
            width=args['width'],
            height=args['height'],
            depth=args['depth'],
            weight=args['weight'],
            capacity=args['capacity'],
            min_temp=args['min_temp'],
            max_temp=args['max_temp'],
            expiration_date=args['expiration_date'],
            calories=args['calories'],
            squirrels=args['squirrels'],
            fats=args['fats'],
            carbohydrates=args['carbohydrates'],
            description=args['description'],
            composition=args['composition']
        )
        # Добавляем товар в БД
        session.add(item)
        # Коммитим
        session.commit()
        session.close()
        # Возвращаем код успешной отправки
        return jsonify({'id': item.id})


def abort_if_item_not_found(item_id):
    """ Если товар не нашелся """
    # Сессия подключения к БД
    session = db_session.create_session()
    # Получаем товар по Id
    item = session.query(Item).get(item_id)
    session.close()
    # Если не нашелся
    if not item:
        # Кидаем ошибку
        abort(404, message=f"Item {item_id} not found")


# Парсер аргументов
parser = reqparse.RequestParser()
# Название
parser.add_argument('name', required=True, type=str)
# Цена
parser.add_argument('price', required=True, type=float)
# Скидка
parser.add_argument('discount', required=True, type=int)
# Поставщик
parser.add_argument('supplier', required=True, type=int)
# Категория
parser.add_argument('category', required=True, type=int)
# Бренд
parser.add_argument('brand', required=False, type=str)
# Тип товара
parser.add_argument('type', required=False, type=str)
# Тип упаковки
parser.add_argument('type_of_packing', required=False, type=str)
# Ширина
parser.add_argument('width', required=False, type=str)
# Высота
parser.add_argument('height', required=False, type=str)
# Глубина
parser.add_argument('depth', required=False, type=str)
# Вес
parser.add_argument('weight', required=False, type=str)
# Ёмкость
parser.add_argument('capacity', required=False, type=str)
# Минимальная температура хранения
parser.add_argument('min_temp', required=True, type=int)
# Максимальная температура хранения
parser.add_argument('max_temp', required=True, type=int)
# Срок годности
parser.add_argument('expiration_date', required=True, type=str)
# Калории
parser.add_argument('calories', required=False, type=str)
# Белки
parser.add_argument('squirrels', required=False, type=str)
# Жиры
parser.add_argument('fats', required=False, type=str)
# Углеводы
parser.add_argument('carbohydrates', required=False, type=str)
# Описание
parser.add_argument('description', required=False, type=str)
# Состав
parser.add_argument('composition', required=False, type=str)