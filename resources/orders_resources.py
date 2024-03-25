from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.orders import Order


class OrdersResource(Resource):
    def get(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        news = session.query(Order).get(order_id)
        return jsonify(
            {'order': news.to_dict(
                only=(
                    'id', 'items_list',
                    'start_date', 'end_date',
                    'is_complited', 'user_id',
                    'user.mobile_phone', 'user.name'
                )
            )}
        )

    def delete(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.query(Order).get(order_id)
        session.delete(order)
        session.commit()
        return jsonify({'success': 'OK'})


class OrdersListResource(Resource):
    """ Получение списка всех заказов, которые имеются """

    def get(self):
        session = db_session.create_session()
        orders = session.query(Order).all()
        return jsonify({
            'orders': [
                item.to_dict(only=(
                    'id', 'items_list', 'is_complited',
                    'user.mobile_phone', 'user.name'
                ))
                for item in orders
            ]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = Order(
            items_list=args['items_list'],
            user_id=args['user_id'],
        )
        session.add(news)
        session.commit()
        return jsonify({'id': news.id})


def abort_if_order_not_found(order_id):
    """ Если заказ не нашелся """
    session = db_session.create_session()
    order = session.query(Order).get(order_id)
    if not order:
        abort(404, message=f"Order {order_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('items_list', required=True)
parser.add_argument('user_id', required=True, type=int)
