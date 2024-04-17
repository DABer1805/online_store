from flask import jsonify, request
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.orders import Order


class OrdersResource(Resource):
    def get(self, order_id):
        """ Получение заказа по Id """
        # Проверяем есть ли такой заказ в БД
        abort_if_order_not_found(order_id)
        # Сессия подключения к БД
        session = db_session.create_session()
        # Получаем заказ
        order = session.query(Order).get(order_id)
        session.close()
        # Возвращаем инфу о заказе
        return jsonify(
            {'order': order.to_dict(
                only=(
                    'id', 'items_list',
                    'start_date', 'end_date',
                    'is_complited', 'user_id',
                    'user.mobile_phone', 'user.name'
                )
            )}
        )

    def delete(self, order_id):
        """ Удаление заказа по Id """
        # Проверяем есть ли такой заказ в БД
        abort_if_order_not_found(order_id)
        # Сессия подключения к БД
        session = db_session.create_session()
        # Получаем заказ по Id
        order = session.query(Order).get(order_id)
        # Удаляем заказ из БД
        session.delete(order)
        # Коммитим
        session.commit()
        session.close()
        # Возвращаем код успешной отправки
        return jsonify({'success': 'OK'})


class OrdersListResource(Resource):
    def get(self):
        """ Получение списка всех заказов, которые имеются """
        # Сессия подключения к БД
        session = db_session.create_session()
        # id пользователя
        user_id = request.args.get('user_id')
        if user_id:
            # Если указан, то получаем заказы только для данного пользователя
            orders = session.query(Order).filter(Order.user_id == user_id)
        else:
            # Иначе, получаем все заказы
            orders = session.query(Order).all()
        session.close()
        # Возвращаем инфу о заказах
        return jsonify({
            'orders': [
                item.to_dict(only=(
                    'id', 'items_list', 'is_complited',
                    'start_date', 'end_date'
                ))
                for item in orders
            ]})

    def post(self):
        """ Добавление заказа """
        # Доступные поля
        args = parser.parse_args()
        # Сессия подключения к БД
        session = db_session.create_session()
        # Создаем обьект заказа
        order = Order(
            items_list=args['items_list'],
            user_id=args['user_id'],
        )
        # Добавляем в БД
        session.add(order)
        # Коммитим
        session.commit()
        session.close()
        # Возвращаем успешный код отправки
        return jsonify({'id': order.id})


def abort_if_order_not_found(order_id):
    """ Если заказ не нашелся """
    # Сессия подключения к БД
    session = db_session.create_session()
    # Получаем заказ по id
    order = session.query(Order).get(order_id)
    session.close()
    # Если не нашелся
    if not order:
        # Кидаем ошибку
        abort(404, message=f"Order {order_id} not found")


# Парсер аргументов
parser = reqparse.RequestParser()
# Список товаров в заказе
parser.add_argument('items_list', required=True)
# Id пользователя
parser.add_argument('user_id', required=True, type=int)
