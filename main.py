import os

from flask import Flask, render_template, redirect, request, url_for
from flask_cors import CORS, cross_origin
from flask_restful import Api
from requests import get, post

from api import calculate_cost_api, user_basket_api, add_item_to_basket_api, \
    del_item_in_basket_api
from data.constants import DB_NAME, TEST_DB_NAME, MAX_PRICE, ALLOWED_EXTENSIONS
from data import db_session
from resources import orders_resources, users_resources, items_resources, \
    categories_resources, suppliers_resources
from data.secret_key import SECRET_KEY

from data.users import User
from data.items import Item
from data.categories import Category
from forms.user import LoginForm, RegisterForm, AddProductForm, \
    AddSupplierForm

from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user

# Задаем конфигурацию приложения
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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

login_manager = LoginManager()
login_manager.init_app(app)

# Подключаем api подсчета цены покупки
app.register_blueprint(calculate_cost_api.blueprint)
# Подключаем api получения товаров из корзины
app.register_blueprint(user_basket_api.blueprint)
# Подключаем api добавления товара в корзину
app.register_blueprint(add_item_to_basket_api.blueprint)
# Подключаем api удаление товара из корзины
app.register_blueprint(del_item_in_basket_api.blueprint)


@app.route('/logout')
@login_required
def logout():
    """ Выход из профиля """
    logout_user()
    # Перевод на страницу с выбором продуктов
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    """ Загрузка пользователя """
    db_sess = db_session.create_session()
    # Возвращаем пользователя
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Авторизация """
    # Создаем форму
    form = LoginForm()
    # Если нажата кнопка авторизации
    if form.validate_on_submit():
        # Создаем сессию подключения к БД
        db_sess = db_session.create_session()
        # Получаем пользователя с введенным номером телефона
        user = db_sess.query(User).filter(
            User.mobile_phone == form.mobile_phone.data
        ).first()
        # Если пароль совпал и пользователь нашелся
        if user and user.check_password(form.password.data):
            # Авторизизуем пользователя
            login_user(user, remember=form.remember_me.data)
            # Перенаправляем пользователя на каталог
            return redirect("catalog")
        # Открываем страничку с формой авторизации и выводим уведомление о
        # некорректности данных
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    # Открываем страничку с формой авторизации
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """ Форма регистрации пользователя """
    # Создаем форму
    form = RegisterForm()
    # Если кнопка нажата
    if form.validate_on_submit():
        # Если пароли не совпали
        if form.password.data != form.password_again.data:
            # Открываем страничку с формой и выводим уведомление о
            # некорректности данных
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # Создаем сессию подключения к БД
        db_sess = db_session.create_session()
        # Проверяем нет ли в БД пользователя с таким номером
        if db_sess.query(User).filter(
                User.mobile_phone == form.mobile_phone.data
        ).first():
            # Открываем страничку с формой и выводим уведомление о
            # некорректности данных
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        # Добавляем в БД нового пользователя
        post(
            'http://localhost:5000/api/users',
            json={
                'name': form.name.data,
                'surname': form.surname.data,
                'items_list': '',
                'mobile_phone': form.mobile_phone.data
            }
        )
        # Получаем этого пользователя
        user = db_sess.query(User).filter(
            User.mobile_phone == form.mobile_phone.data
        ).first()
        # Устанавливаем ему хэшированный пароль
        user.set_password(form.password.data)
        # Делаем коммит
        db_sess.commit()
        # Перенаправляем на форму авторизации
        return redirect('/login')
    # Открываем страничку с формой регистрации
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/catalog", methods=['GET', 'POST'])
@cross_origin()
def catalog():
    """ Каталог с товарами """
    # Параметры
    params = {}
    # Нажатые чекбоксы
    checked_buttons = []
    # Получаем категории, которые были переданы через параметры URL
    cat = request.args.get('cat')
    # Получаем через параметр URL цену, которая была выбрана пользователем
    # на слайдере
    cur_price = request.args.get('max_price')
    # Если в параметре цена не указана
    if cur_price is None:
        # Устанавливаем цену как максимальную
        cur_price = MAX_PRICE
    cat_filters = None
    # Если категории переданы через параметры
    if cat:
        # Устанавливаем в параметрах эти категории
        params['cat'] = cat
        # Добавляем в список нажатых кнопок эти категории
        checked_buttons += list(map(int, cat.split(',')))
        cat_filters = ', '.join(
            map(lambda x: get(
                f'http://localhost:5000/api/categories/{x}'
            ).json()['name'], cat.split(','))
        )
    # Устанавливаем в параметрах ограничение по цене - текущую цену на
    # слайдере
    params['max_price'] = cur_price
    # Если нажата кнопка фильтрации
    if request.method == 'POST':
        # Перенаправляем пользователя на каталог уже вместе с параметрами
        return redirect(
            f'/catalog?cat={",".join(request.form.getlist("cat"))}&'
            f'max_price={request.form.get("price_range")}'
        )
    # Проверяем, авторизован ли пользователь, и если да, то получаем список
    # тех товаров, которые он выбрал
    if current_user.is_authenticated:
        items_list = current_user.items_list
    else:
        items_list = ''
    # Получаем список товаров, которые лежат в корзине пользователя,
    # включая количество товаров
    user_basket = get(
        'http://localhost:5000/api/user_basket',
        params={'items_list': items_list}
    ).json()['items']
    # Получаем список всех товаров с учетом параметров
    items = get(
        'http://localhost:5000/api/items', params=params
    ).json()['items']
    # Получаем список всех категорий
    categories = get(
        'http://localhost:5000/api/categories'
    ).json()['items']
    # Открываем страничку с каталогом
    return render_template(
        "items_list.html", title='Продуктовый рай', cur_price=cur_price,
        checked_buttons=checked_buttons, items=items, categories=categories,
        cat_filters=cat_filters, max_price=MAX_PRICE, user_basket=user_basket
    )


@app.route("/catalog/<int:item_id>")
def item_page(item_id):
    # Получаем инфо о выбранном предмете
    item = get(f'http://localhost:5000/api/items/{item_id}').json()['item']
    # Категории предыдущей страницы каталога
    cat = request.args.get('cat')
    # Если открыта страница товара не из каталога
    anchor = request.args.get('anchor')
    # Максимальная цена фильтра каталога при открытии страницы товара
    max_price = request.args.get('max_price')
    # ЕСли параметр максимальной цены не передан, то устанавливаем дефолтное
    if max_price is None:
        max_price = MAX_PRICE
    # Если переданы категории предыдущей страницы каталога
    if cat:
        categories = {
            'names': ', '.join(map(lambda x: get(
                f'http://localhost:5000/api/categories/{x}'
            ).json()['name'], cat.split(','))),
            'ids': cat
        }
    else:
        categories = {}
    # Проверяем, авторизован ли пользователь, и если да, то получаем список
    # тех товаров, которые он выбрал
    if current_user.is_authenticated:
        items_list = current_user.items_list
    else:
        items_list = ''
    # Получаем список товаров, которые лежат в корзине пользователя,
    # включая количество товаров
    user_basket = get(
        'http://localhost:5000/api/user_basket',
        params={'items_list': items_list}
    ).json()['items']
    return render_template(
        "item_page.html", title='Продуктовый рай', item=item,
        categories=categories, max_price=max_price, anchor=anchor,
        user_basket=user_basket
    )


@app.route("/")
def home_page():
    slides = os.listdir(url_for("static", filename="img/slides")[1:])
    discounted_items = get(
        'http://localhost:5000/api/items', params={'only_discount': True}
    ).json()['items']
    # Проверяем, авторизован ли пользователь, и если да, то получаем список
    # тех товаров, которые он выбрал
    if current_user.is_authenticated:
        items_list = current_user.items_list
    else:
        items_list = ''
    # Получаем список товаров, которые лежат в корзине пользователя,
    # включая количество товаров
    user_basket = get(
        'http://localhost:5000/api/user_basket',
        params={'items_list': items_list}
    ).json()['items']
    return render_template(
        "index.html", title='Продуктовый рай', slides=slides,
        categories=CATEGORIES, discounted_items=discounted_items,
        user_basket=user_basket
    )


@app.route("/add_product", methods=['GET', 'POST'])
def add_product_page():
    """Страничка добавления товара"""

    # создание формы добавления товаров
    form = AddProductForm()

    session = db_session.create_session()

    # Проверка id пользователя (доступ только для id == 1)
    if int(current_user.get_id()) == 1:
        # Если нажата кнопка отправки формы
        if form.validate_on_submit():
            # Есть ли наше изображение в переданном запросе
            if 'product_image' in request.files:
                # Имя файла с изображением
                image = request.files['product_image']
                # Проверка формата файла:
                if image.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
                    # Определяем имя файла на основе id последнего товара в бд
                    id_amount = len(session.query(Item.id).all())
                    filename = f"item{id_amount + 1}.png"
                    # Здесь указывается путь до папки на сервере,
                    # где будет сохранен файл
                    path_to_save = os.path.join('./static/img/items', filename)
                    image.save(path_to_save)
                else:
                    return render_template(
                        'add_product.html', title="Страница управления", form=form,
                        message="Недопустимый формат изображения"
                    )
            # добавляем товар
            post(
                'http://localhost:5000/api/items',
                json={
                    "name": form.name.data,
                    "price": float(form.cost.data),
                    "discount": int(form.discount.data),
                    "supplier": 1,
                    "category": session.query(Category).filter(
                        Category.name == form.category.data
                    ).first().id
                }
            )
        # при ошибке ввода цены
        elif form.cost.data is None and request.files:
            return render_template(
                'add_product.html', title="Страница управления", form=form,
                cost_error=True
            )

        return render_template(
            'add_product.html', title="Страница управления", form=form
        )


@app.route("/add_supplier", methods=['GET', 'POST'])
def add_supplier_page():
    """Страничка добавления товара"""

    # создание формы добавления товаров
    form = AddSupplierForm()

    session = db_session.create_session()

    # Проверка id пользователя (доступ только для id == 1)
    if int(current_user.get_id()) == 1:
        # Если нажата кнопка отправки формы
        if form.validate_on_submit():

            # регистрируем поставщика
            post(
                'http://localhost:5000/api/suppliers',
                json={
                    "name": form.name.data,
                    "payment_account": form.payment_account.data,
                    "address": form.payment_account.data,
                    "mobile_phone": form.mobile_phone.data,
                    "email": form.email.data
                }
            )

        return render_template(
            'add_supplier.html', title="Регистрация поставщика", form=form
        )


def main():
    # Устанавливаем соедениние с БД
    db_session.global_init(f'db/{TEST_DB_NAME}')
    # Запускаем предложение
    app.run()


if __name__ == '__main__':
    main()
