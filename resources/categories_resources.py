from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.categories import Category


class CategoriesResource(Resource):
    def get(self, category_id):
        """ Получение категории по ID """
        # Проверяем, есть ли категория с таким ID
        abort_if_category_not_found(category_id)
        # Делаем запрос к БД и получаем категорию по ID
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        # Возвращаем информацию о категории в json формате
        return jsonify(
            {'categories': category.to_dict(only=('id', 'name', 'items.id'))}
        )

    def delete(self, category_id):
        """ Удаление категории по ID """
        # Проверяем, есть ли категория с таким ID
        abort_if_category_not_found(category_id)
        # Делаем запрос к БД и получаем категорию по ID
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        # Удаляем из БД полученную категорию
        session.delete(category)
        # Делаем коммит
        session.commit()
        # Возвращаем отчет об успешном удалении
        return jsonify({'success': 'OK'})


class CategoriesListResource(Resource):
    """ Получение списка всех товаров, которые имеются """

    def get(self):
        """ Получение списка категорий """
        # Делаем запрос к БД и получаем список категорий
        session = db_session.create_session()
        categories = session.query(Category).all()
        # Возвращаем информацию о категориях в json формате
        return jsonify({
            'items': [
                item.to_dict(only=('id', 'name'))
                for item in categories
            ]})

    def post(self):
        """ Добавление новой категории """
        args = parser.parse_args()
        # Делаем запрос к БД и формируем объект категории
        session = db_session.create_session()
        category = Category(
            name=args['name'],
        )
        # Добавляем категорию в БД
        session.add(category)
        # Делаем коммит
        session.commit()
        # Возвращаем ID новой категории
        return jsonify({'id': category.id})


def abort_if_category_not_found(category_id):
    """ Если категория не нашлась """
    session = db_session.create_session()
    category = session.query(Category).get(category_id)
    if not category:
        abort(404, message=f"Category {category_id} not found")


# Парсер аргументов новой категории
parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
