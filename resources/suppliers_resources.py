from flask import jsonify
from flask_restful import Resource, reqparse, abort

from data import db_session
from data.suppliers import Supplier


class SupplierResource(Resource):
    def get(self, supplier_id):
        abort_if_supplier_not_found(supplier_id)
        session = db_session.create_session()
        supplier = session.query(Supplier).get(supplier_id)
        return jsonify(
            {'user': supplier.to_dict(
                only=(
                    'id', 'name', 'payment_account',
                    'address', 'mobile_phone',
                    'email', 'items.id'
                )
            )}
        )

    def delete(self, supplier_id):
        abort_if_supplier_not_found(supplier_id)
        session = db_session.create_session()
        supplier = session.query(Supplier).get(supplier_id)
        session.delete(supplier)
        session.commit()
        return jsonify({'success': 'OK'})


class SupplierListResource(Resource):
    """ Получение списка всех пользователей, которые имеются """

    def get(self):
        session = db_session.create_session()
        suppliers = session.query(Supplier).all()
        return jsonify({
            'suppliers': [
                item.to_dict(only=(
                    'id', 'name', 'payment_account',
                    'mobile_phone'
                ))
                for item in suppliers
            ]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        supplier = Supplier(
            name=args['name'],
            payment_account=args['payment_account'],
            address=args['address'],
            mobile_phone=args['mobile_phone'],
            email=args['email']
        )
        session.add(supplier)
        session.commit()
        return jsonify({'id': supplier.id})


def abort_if_supplier_not_found(supplier_id):
    """ Если поставщик не нашелся """
    session = db_session.create_session()
    supplier = session.query(Supplier).get(supplier_id)
    if not supplier:
        abort(404, message=f"Supplier {supplier_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('payment_account', required=True)
parser.add_argument('address', required=True)
parser.add_argument('mobile_phone', required=True)
parser.add_argument('email', required=True)
