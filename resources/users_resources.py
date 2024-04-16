from flask import jsonify
from flask_restful import Resource, reqparse, abort

from data import db_session
from data.users import User


class UsersResource(Resource):
    def get(self, user_id):
        """ Получение пользователя по Id """
        # Проверяем есть ли такой пользователь в БД
        abort_if_user_not_found(user_id)
        # Сессия подключения к БД
        session = db_session.create_session()
        # Пользователь
        user = session.query(User).get(user_id)
        # Возвращаем инфу о пользователе
        return jsonify(
            {'user': user.to_dict(
                only=(
                    'id', 'surname', 'name',
                    'items_list', 'mobile_phone'
                )
            )}
        )

    def delete(self, user_id):
        """ Удаление пользователя по Id """
        # Проверяем есть ли такой пользователь в БД
        abort_if_user_not_found(user_id)
        # Сессия подключения к БД
        session = db_session.create_session()
        # Пользователь
        user = session.query(User).get(user_id)
        # Удаляем из БД пользователя с таким Id
        session.delete(user)
        # Коммитим
        session.commit()
        # Возвращаем код успешной операции
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        """ Получение списка всех пользователей, которые имеются """
        # Сессия подключения к БД
        session = db_session.create_session()
        # Пользователи
        users = session.query(User).all()
        # Возвращаем инфу о пользователях
        return jsonify({
            'users': [
                item.to_dict(only=(
                    'id', 'surname', 'name', 'items_list', 'mobile_phone'
                ))
                for item in users
            ]})

    def post(self):
        """ Добавление пользователя в БД """
        # Доступные поля
        args = parser.parse_args()
        # Сессия подключения к БД
        session = db_session.create_session()
        # Создаем объект пользователя
        user = User(
            surname=args['surname'],
            name=args['name'],
            items_list=args['items_list'],
            mobile_phone=args['mobile_phone']
        )
        # Добавляем в БД
        session.add(user)
        # Коммитим
        session.commit()
        return jsonify({'id': user.id})


def abort_if_user_not_found(user_id):
    """ Если пользователь не нашелся """
    # Сессия подключения к БД
    session = db_session.create_session()
    # Получаем заказ
    order = session.query(User).get(user_id)
    # Если заказ не нашелся
    if not order:
        # Кидаем ошибку
        abort(404, message=f"User {user_id} not found")


# Парсер аргументов
parser = reqparse.RequestParser()
# Фамилия
parser.add_argument('surname', required=True)
# Имя
parser.add_argument('name', required=True)
# Корзина
parser.add_argument('items_list', required=True)
# Номер мобильного телефона
parser.add_argument('mobile_phone', required=True)
