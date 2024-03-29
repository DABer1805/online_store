import flask
from flask import jsonify

from data import db_session
from data.items import Item
from data.users import User

blueprint = flask.Blueprint('add_item_to_basket_api', __name__)


@blueprint.route('/api/add_item_to_basket/<int:item_id>/<int:user_id>')
def add_item_to_basket(item_id, user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    user_items_list = user.items_list
    if user_items_list:
        new_items_list = {key: value for key, value in map(
            lambda y: map(int, y.split('x')), user_items_list.split(',')
        )}

        if item_id in new_items_list:
            new_items_list[item_id] += 1
        else:
            new_items_list[item_id] = 1

        user.items_list = ','.join(
            map(lambda x: 'x'.join(map(str, x)), new_items_list.items())
        )
    else:
        user.items_list = f'{item_id}x1'
        new_items_list = {item_id: 1}

    session.commit()
    item = session.query(Item).get(item_id)

    return jsonify(
        {
            'item': item.to_dict(only=(
                'name', 'price', 'discount'
            )),
            'amount': new_items_list[item_id]
        }
    )
