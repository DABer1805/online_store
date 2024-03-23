from flask import Flask
from flask_restful import Api

from api import calculate_cost_api
from data.constants import TEST_DB_NAME
from data import db_session
from resources import orders_resources, users_resources, items_resources, \
    categories_resources, suppliers_resources
from data.secret_key import SECRET_KEY

# Задаем конфигурацию приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
api = Api(app)

# Добавляем ресурс для получения списка всех заказов или для добавления
# нового заказа
api.add_resource(orders_resources.OrdersListResource, '/api/orders')
# Добавляем ресурс для получения заказа по ID или для удаления заказа по ID
api.add_resource(orders_resources.OrdersResource,
                 '/api/orders/<int:order_id>')
# Добавляем ресурс для получения списка всех пользователей или для добавления
# нового пользователя
api.add_resource(users_resources.UsersListResource, '/api/users')
# Добавляем ресурс для получения пользователя по ID или удаления
# пользователя по ID
api.add_resource(users_resources.UsersResource, '/api/users/<int:user_id>')
# Добавляем ресурс для получения списка всех товаров или для добавления
# нового товара
api.add_resource(items_resources.ItemsListResource, '/api/items')
# Добавляем ресурс для получения товара по ID или удаления
# товара по ID
api.add_resource(items_resources.ItemsResource, '/api/items/<int:item_id>')
# Добавляем ресурс для получения списка всех категорий или для добавления
# новой категории
api.add_resource(categories_resources.CategoriesListResource,
                 '/api/categories')
# Добавляем ресурс для получения категории по ID или удаления
# категории по ID
api.add_resource(categories_resources.CategoriesResource,
                 '/api/categories/<int:category_id>')
# Добавляем ресурс для получения списка всех поставщиков или для добавления
# нового поставщика
api.add_resource(suppliers_resources.SupplierListResource,
                 '/api/suppliers')
# Добавляем ресурс для получения поставщика по ID или удаления
# поставщика по ID
api.add_resource(suppliers_resources.SupplierResource,
                 '/api/suppliers/<int:supplier_id>')


def main():
    db_session.global_init(f'db/{TEST_DB_NAME}')
    app.register_blueprint(calculate_cost_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
