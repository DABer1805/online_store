import flask
from flask import jsonify

from requests import get

from data import db_session
from data.orders import Order
from data.users import User

blueprint = flask.Blueprint('make_order_api', __name__)


@blueprint.route('/api/make_order/<int:user_id>')
def make_order(user_id):
    # Сессия подключения к БД
    session = db_session.create_session()
    # Получаем информацию о пользователе
    user = session.query(User).get(user_id)
    if user.items_list:
        # Создаем новый заказ
        order = Order()
        # Помещаем текущую корзину пользователя в список заказов
        order.items_list = user.items_list
        # Записываем ID пользователя
        order.user_id = user.id
        # Кидаем в БД
        session.add(order)
        # Опусташаем корзину
        user.items_list = None
        # Коммитим
        session.commit()
        session.close()

        return jsonify({'status': 'OK'})
    return jsonify({'status': 'FAIL'})
