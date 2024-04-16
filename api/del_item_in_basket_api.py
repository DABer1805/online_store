import flask
from flask import jsonify

from data import db_session
from data.items import Item
from data.users import User

blueprint = flask.Blueprint('del_item_in_basket_api', __name__)


@blueprint.route('/api/del_item_in_basket_api/<int:item_id>/<int:user_id>')
def del_item_in_basket(item_id, user_id):
    # Сессия подключения к БД
    session = db_session.create_session()
    # Получаем нашего пользователя
    user = session.query(User).get(user_id)
    # Достаем его список продуктов
    user_items_list = user.items_list
    # Если список не пуст
    if user_items_list:
        # Переделываем строку в словарь (id товара: кол-во товара)
        new_items_list = {key: value for key, value in map(
            lambda y: map(int, y.split('x')), user_items_list.split(',')
        )}

        # Если товар есть в корзине
        if item_id in new_items_list:
            if new_items_list[item_id] > 1:
                # Если товара больше чем 1, то просто отнимаем кол-во на 1
                new_items_list[item_id] -= 1
            else:
                # В ином случае, полностью удаляем данный товара из списка
                del new_items_list[item_id]

            # Собираем список обратно в строку
            user.items_list = ','.join(
                map(lambda x: 'x'.join(map(str, x)), new_items_list.items())
            )

            # Коммитим
            session.commit()
            # Получаем данный товар
            item = session.query(Item).get(item_id)
            # Количество данного товара
            amount = new_items_list.get(item_id)

            # Возвращам инфу о товаре после удаления
            return jsonify(
                {
                    'item': item.to_dict(only=(
                        'name', 'price', 'discount'
                    )),
                    'amount': amount if amount else 0
                }
            )
    # Если товара в корзине не оказалось
    return jsonify({'error': 'item not in basket'})