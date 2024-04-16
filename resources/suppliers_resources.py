from flask import jsonify
from flask_restful import Resource, reqparse, abort

from data import db_session
from data.suppliers import Supplier


class SupplierResource(Resource):
    def get(self, supplier_id):
        """ Получение поставщика по Id """
        # Проверяем есть ли такой поставщик в БД
        abort_if_supplier_not_found(supplier_id)
        # Сессия подключения к БД
        session = db_session.create_session()
        # Поставщик
        supplier = session.query(Supplier).get(supplier_id)
        # Возвращаем инфу о поставщике
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
        """ Удаление поставщика по Id """
        # Проверяем есть ли такой поставщик в БД
        abort_if_supplier_not_found(supplier_id)
        # Сессия подключения к БД
        session = db_session.create_session()
        # Поставщик
        supplier = session.query(Supplier).get(supplier_id)
        # Удаляем поставщика
        session.delete(supplier)
        # Коммитим
        session.commit()
        # Возвращаем код успешной отправки
        return jsonify({'success': 'OK'})


class SupplierListResource(Resource):
    def get(self):
        """ Получение списка всех поставщиков, которые имеются """
        # Сессия подключения к БД
        session = db_session.create_session()
        # Поставщики
        suppliers = session.query(Supplier).all()
        # Возвращаем инфу о поставщиках
        return jsonify({
            'suppliers': [
                item.to_dict(only=(
                    'id', 'name', 'payment_account',
                    'mobile_phone'
                ))
                for item in suppliers
            ]})

    def post(self):
        """ Получение списка всех поставщиков, которые имеются """
        # Аргументы парсера
        args = parser.parse_args()
        # Сессия подключения к БД
        session = db_session.create_session()
        #  Создаем объект поставщика
        supplier = Supplier(
            name=args['name'],
            payment_account=args['payment_account'],
            address=args['address'],
            mobile_phone=args['mobile_phone'],
            email=args['email']
        )
        # Добавляем поставщика в БД
        session.add(supplier)
        # Коммитим
        session.commit()
        # Возвращаем код успешной отправки
        return jsonify({'id': supplier.id})


def abort_if_supplier_not_found(supplier_id):
    """ Если поставщик не нашелся """
    # Сессия подключения к БД
    session = db_session.create_session()
    # Поставщик
    supplier = session.query(Supplier).get(supplier_id)
    # Если поставщик не нашелся
    if not supplier:
        # Кидаем ошибку
        abort(404, message=f"Supplier {supplier_id} not found")


#  Парсер аргументов
parser = reqparse.RequestParser()
# Название
parser.add_argument('name', required=True)
# Расчетный счет
parser.add_argument('payment_account', required=True)
# Адрес
parser.add_argument('address', required=True)
# Номер мобильного телефона
parser.add_argument('mobile_phone', required=True)
# Электронная почта
parser.add_argument('email', required=True)
