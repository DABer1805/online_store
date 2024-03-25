from flask import jsonify
from flask_restful import Resource, reqparse, abort

from data import db_session
from data.users import User


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {'user': user.to_dict(
                only=(
                    'id', 'surname', 'name',
                    'items_list', 'mobile_phone'
                )
            )}
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    """ Получение списка всех пользователей, которые имеются """

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'users': [
                item.to_dict(only=(
                    'id', 'items_list', 'mobile_phone'
                ))
                for item in users
            ]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            items_list=args['items_list'],
            mobile_phone=args['mobile_phone']
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})


def abort_if_user_not_found(user_id):
    """ Если пользователь не нашелся """
    session = db_session.create_session()
    order = session.query(User).get(user_id)
    if not order:
        abort(404, message=f"User {user_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('items_list', required=True)
parser.add_argument('mobile_phone', required=True)
