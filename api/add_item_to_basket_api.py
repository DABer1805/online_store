import flask
from flask import jsonify

from data import db_session
from data.items import Item
from data.users import User

blueprint = flask.Blueprint('add_item_to_basket_api', __name__)


@blueprint.route('/api/add_item_to_basket/<int:item_id>/<int:user_id>')
def add_item_to_basket(item_id, user_id):
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
            # Если товар уже имеется, то просто увеличиваем его кол-во на 1
            new_items_list[item_id] += 1
        else:
            # В ином случае создаем новую запись с кол-вом = 1
            new_items_list[item_id] = 1

        # Собираем список обратно в строку
        user.items_list = ','.join(
            map(lambda x: 'x'.join(map(str, x)), new_items_list.items())
        )
    else:
        # Если корзина пуста, то собираем сразу строку
        user.items_list = f'{item_id}x1'
        new_items_list = {item_id: 1}

    # Коммитим
    session.commit()
    # Получаем данный товар
    item = session.query(Item).get(item_id)

    # Возвращам инфу о товаре после добавления
    return jsonify(
        {
            'item': item.to_dict(only=(
                'name', 'price', 'discount'
            )),
            'amount': new_items_list[item_id]
        }
    )
