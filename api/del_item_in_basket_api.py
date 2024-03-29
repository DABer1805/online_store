import flask
from flask import jsonify

from data import db_session
from data.items import Item
from data.users import User

blueprint = flask.Blueprint('del_item_in_basket_api', __name__)


@blueprint.route('/api/del_item_in_basket_api/<int:item_id>/<int:user_id>')
def del_item_in_basket(item_id, user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    user_items_list = user.items_list
    if user_items_list:
        new_items_list = {key: value for key, value in map(
            lambda y: map(int, y.split('x')), user_items_list.split(',')
        )}

        if item_id in new_items_list:
            if new_items_list[item_id] > 1:
                new_items_list[item_id] -= 1
            else:
                del new_items_list[item_id]

            user.items_list = ','.join(
                map(lambda x: 'x'.join(map(str, x)), new_items_list.items())
            )

            session.commit()
            item = session.query(Item).get(item_id)
            amount = new_items_list.get(item_id)

            return jsonify(
                {
                    'item': item.to_dict(only=(
                        'name', 'price', 'discount'
                    )),
                    'amount': amount if amount else 0
                }
            )
    return jsonify({'error': 'item not in basket'})