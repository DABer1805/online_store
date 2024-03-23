import flask
from flask import jsonify

from data import db_session
from data.orders import Order

from requests import get

blueprint = flask.Blueprint('calculate_cost_api', __name__)


def get_position_total_cost(item_id, amount):
    item = get(f'http://localhost:5000/api/items/{item_id}').json()['item']
    price, discount = item['price'], item['discount']
    if discount:
        price *= 1 - discount * 0.01
    return price * amount


@blueprint.route('/api/calculate/<int:order_id>')
def calculate_cost(order_id):
    session = db_session.create_session()
    order = session.query(Order).get(order_id)
    total = sum(
        map(
            lambda x: get_position_total_cost(int(x[0]), int(x[1])),
            map(
                lambda y: y.split('x'),
                order.items_list.split(',')
            )
        )
    )
    return jsonify({'total': total})
