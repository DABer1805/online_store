import flask
from flask import jsonify, request

from requests import get

blueprint = flask.Blueprint('user_basket_api', __name__)


@blueprint.route('/api/user_basket')
def user_basket():
    # Общая цена всех товаров в корзине
    total = 0
    # Список товаров, которые выбрал пользователь
    items_list = request.args.get('items_list')
    # Информация о таврах, которые выбрал пользователь
    items = []
    if items_list:
        for item_id, amount in map(
                lambda x: x.split('x'), items_list.split(',')
        ):
            cur_item = {}
            # Информация о текущем товаре
            item = get(
                f'http://{request.host}/api/items/{item_id}'
            ).json()['item']
            price = item['price']
            discount = item['discount']
            total += price * (1 - discount * 0.01) * int(amount)
            cur_item['item'] = item
            # Информация о количестве выбранного товара
            cur_item['amount'] = amount
            # Добавляем данные в итоговый список
            items.append(cur_item)
    return jsonify({'items': items, 'total': round(total, 2)})
