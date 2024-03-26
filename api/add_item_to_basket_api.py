import flask
from flask import jsonify
from flask_login import current_user

from data import db_session
from data.items import Item
from data.users import User

blueprint = flask.Blueprint('add_item_to_basket_api', __name__)


@blueprint.route('/api/add_item_to_basket/<int:item_id>')
def add_item_to_basket(item_id):
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    user_items_list = user.items_list
    if user_items_list:
        items_list = {key: value for key, value in map(
            lambda y: map(int, y.split('x')), user_items_list.split(',')
        )}

        if item_id in items_list:
            items_list[item_id] += 1
        else:
            items_list[item_id] = 1

        user.items_list = ','.join(
            map(lambda x: 'x'.join(map(str, x)), items_list.items())
        )
    else:
        user.items_list = f'{item_id}x1'

    session.commit()

    item = session.query(Item).get(item_id)
    item_name = item.name

    return jsonify({'item': item_name})
