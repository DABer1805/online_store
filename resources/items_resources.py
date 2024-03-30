from flask import jsonify
from flask_restful import Resource, abort, reqparse, request

from data import db_session
from data.constants import MAX_PRICE
from data.items import Item


class ItemsResource(Resource):
    def get(self, item_id):
        abort_if_item_not_found(item_id)
        session = db_session.create_session()
        item = session.query(Item).get(item_id)
        return jsonify(
            {'item': item.to_dict(only=(
                'id', 'name', 'price', 'discount',
                'supplier', 'category'
            ))}
        )

    def delete(self, item_id):
        abort_if_item_not_found(item_id)
        session = db_session.create_session()
        item = session.query(Item).get(item_id)
        session.delete(item)
        session.commit()
        return jsonify({'success': 'OK'})


class ItemsListResource(Resource):
    """ Получение списка всех товаров, которые имеются """

    def get(self):
        categories = request.args.get('cat')
        max_price = request.args.get('max_price')
        only_discount = request.args.get('only_discount')
        if max_price is None:
            max_price = MAX_PRICE
        else:
            max_price = float(max_price)

        session = db_session.create_session()
        if only_discount:
            items = session.query(Item).filter(Item.discount > 0)
        elif categories:
            categories = list(map(int, categories.split(',')))
            items = session.query(Item).filter(
                Item.category.in_(categories),
                Item.price * (1 - Item.discount * 0.01) <= max_price
            )
        else:
            items = session.query(Item).filter(
                Item.price * (1 - Item.discount * 0.01) <= max_price
            )
        return jsonify({
            'items': [
                item.to_dict(only=('id', 'name', 'price', 'discount'))
                for item in items
            ]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        item = Item(
            name=args['name'],
            price=args['price'],
            discount=args['discount'],
            supplier=args['supplier'],
            category=args['category']
        )
        session.add(item)
        session.commit()
        return jsonify({'id': item.id})


def abort_if_item_not_found(item_id):
    """ Если товар не нашелся """
    session = db_session.create_session()
    item = session.query(Item).get(item_id)
    if not item:
        abort(404, message=f"Item {item_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('price', required=True, type=int)
parser.add_argument('discount', required=True, type=int)
parser.add_argument('supplier', required=True, type=int)
parser.add_argument('category', required=True, type=int)
