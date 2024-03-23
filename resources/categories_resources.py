from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.categories import Category


class CategoriesResource(Resource):
    def get(self, category_id):
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        print(category)
        return jsonify(
            {'categories': category.to_dict(only=('name', 'items.id'))}
        )

    def delete(self, category_id):
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        session.delete(category)
        session.commit()
        return jsonify({'success': 'OK'})


class CategoriesListResource(Resource):
    """ Получение списка всех товаров, которые имеются """

    def get(self):
        session = db_session.create_session()
        category = session.query(Category).all()
        return jsonify({
            'items': [
                item.to_dict(only=('name', ))
                for item in category
            ]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        category = Category(
            name=args['name'],
        )
        session.add(category)
        session.commit()
        return jsonify({'id': category.id})


def abort_if_category_not_found(category_id):
    """ Если категория не нашлась """
    session = db_session.create_session()
    category = session.query(Category).get(category_id)
    if not category:
        abort(404, message=f"Category {category_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
