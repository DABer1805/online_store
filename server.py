import os

from PIL import Image
from flask import Flask, render_template, redirect, request, url_for
from flask_cors import CORS, cross_origin
from flask_restful import Api, abort
from requests import get, post

from api import user_basket_api, add_item_to_basket_api, \
    del_item_in_basket_api, make_order_api
from data.constants import DB_NAME, TEST_DB_NAME, MAX_PRICE, \
    ALLOWED_EXTENSIONS, CATEGORIES
from data import db_session
from data.suppliers import Supplier
from resources import orders_resources, users_resources, items_resources, \
    categories_resources, suppliers_resources
from data.secret_key import SECRET_KEY

from data.users import User
from data.items import Item
from data.categories import Category
from forms.user import LoginForm, RegisterForm
from forms.admin import AddProductForm, AddSupplierForm

from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user

# При хостинге необходимо http протоколы заменить на https, чтобы все
# корректно работало )))

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

# Подключаем api получения товаров из корзины
app.register_blueprint(user_basket_api.blueprint)
# Подключаем api добавления товара в корзину
app.register_blueprint(add_item_to_basket_api.blueprint)
# Подключаем api удаление товара из корзины
app.register_blueprint(del_item_in_basket_api.blueprint)
# Подключаем api для выполнения заказа
app.register_blueprint(make_order_api.blueprint)


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
            if user.id == 1:
                # Перенаправляем пользователя на админку
                return redirect("/admin")
            # Перенаправляем пользователя на каталог
            return redirect("/")
        # Открываем страничку с формой авторизации и выводим уведомление о
        # некорректности данных
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    # Открываем страничку с формой авторизации
    return render_template(
        'login.html', title='Авторизация', host_data=request.host, form=form
    )


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
            return render_template(
                'register.html', title='Регистрация', host_data=request.host,
                form=form, message="Пароли не совпадают"
            )
        # Создаем сессию подключения к БД
        db_sess = db_session.create_session()
        # Проверяем нет ли в БД пользователя с таким номером
        if db_sess.query(User).filter(
                User.mobile_phone == form.mobile_phone.data
        ).first():
            # Открываем страничку с формой и выводим уведомление о
            # некорректности данных
            return render_template(
                'register.html', title='Регистрация', host_data=request.host,
                form=form, message="Такой пользователь уже есть"
            )
        # Добавляем в БД нового пользователя
        post(
            f'http://{request.host}/api/users',
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
    return render_template(
        'register.html', title='Регистрация', host_data=request.host,
        form=form
    )


@app.route('/change_user_data', methods=['GET', 'POST'])
def change_user_data():
    """ Редактирование данных пользователя """
    if current_user.is_authenticated and current_user.id == 1:
        # Админ не должен попасть на эту страницу
        abort(404, message=f"No access rights")
    form = RegisterForm()
    # Подгрузка текущей инфы в поля формочки
    if request.method == "GET":
        # Сессия подключения к БД
        db_sess = db_session.create_session()
        # Достаём нашего пользователя из БД
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        # Если нашелся
        if user:
            # Заполяняем поле с номером телефона
            form.mobile_phone.data = user.mobile_phone
            # Заполяняем поле с фамилией
            form.surname.data = user.surname
            # Заполяняем поле с именем
            form.name.data = user.name
        else:
            # Кидаем ошибку
            abort(404)
    # Если пользователь нажал на кнопку
    if form.validate_on_submit():
        # Сессия подключения к БД
        db_sess = db_session.create_session()
        # Достаём нашего пользователя из БД
        user = db_sess.query(User).filter(
            User.id == current_user.id
        ).first()
        # Если нашелся
        if user:
            # Пароли не совпали
            if form.password.data != form.password_again.data:
                # Открываем страничку с формой и выводим уведомление о
                # некорректности данных
                return render_template(
                    'register.html', title='Регистрация', form=form,
                    message="Пароли не совпадают"
                )
            # Проверяем нет ли в БД пользователя с таким номером
            if db_sess.query(User).filter(
                    User.mobile_phone == form.mobile_phone.data
            ).count() > 1:
                # Открываем страничку с формой и выводим уведомление о
                # некорректности данных
                return render_template(
                    'register.html', title='Регистрация',
                    host_data=request.host, form=form,
                    message="Такой пользователь уже есть"
                )
            # Переприсваиваем поле с номером телефона
            user.mobile_phone = form.mobile_phone.data
            # Переприсваиваем поле с фамилией
            user.surname = form.surname.data
            # Переприсваиваем поле с именем
            user.name = form.name.data
            # Устанавливаем новый пароль
            user.set_password(form.password.data)
            # Коммитим
            db_sess.commit()
            # Перенаправляем в личный кабинет
            return redirect('/personal_account')
        else:
            # Кидаем ошибку
            abort(404)
    # Открываем страничку с формочкой
    return render_template(
        'register.html', title='Регистрация', host_data=request.host,
        form=form
    )


@app.route("/catalog", methods=['GET', 'POST'])
@cross_origin()
def catalog():
    """ Каталог с товарами """
    # Проверяем, авторизован ли пользователь, и если да, то получаем список
    # тех товаров, которые он выбрал
    if current_user.is_authenticated:
        # Админ не должен попасть на эту страницу
        if current_user.id == 1:
            abort(404, message=f"No access rights")
        items_list = current_user.items_list
    else:
        items_list = ''
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
                f'http://{request.host}/api/categories/{x}'
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
    # Получаем список товаров, которые лежат в корзине пользователя,
    # включая количество товаров
    user_basket_info = get(
        f'http://{request.host}/api/user_basket',
        params={'items_list': items_list}
    ).json()
    user_basket = user_basket_info['items']
    total = user_basket_info['total']
    # Получаем список всех товаров с учетом параметров
    items = get(
        f'http://{request.host}/api/items', params=params
    ).json()['items']
    # Получаем список всех категорий
    categories = get(
        f'http://{request.host}/api/categories'
    ).json()['items']
    # Открываем страничку с каталогом
    return render_template(
        "items_list.html", title='Продуктовый рай', host_data=request.host,
        cur_price=cur_price, checked_buttons=checked_buttons, items=items,
        categories=categories, cat_filters=cat_filters,
        max_price=MAX_PRICE, user_basket=user_basket, total=total
    )


@app.route("/catalog/<int:item_id>")
def item_page(item_id):
    # Проверяем, авторизован ли пользователь, и если да, то получаем список
    # тех товаров, которые он выбрал
    if current_user.is_authenticated:
        # Админ не должен попасть на эту страницу
        if current_user.id == 1:
            abort(404, message=f"No access rights")
        items_list = current_user.items_list
    else:
        items_list = ''
    # Получаем инфо о выбранном предмете
    item = get(f'http://{request.host}/api/items/{item_id}').json()['item']
    # Категории предыдущей страницы каталога
    cat = request.args.get('cat')
    # Если открыта страница товара из каталога
    from_catalog = request.args.get('from_catalog')
    # Максимальная цена фильтра каталога при открытии страницы товара
    max_price = request.args.get('max_price')
    # ЕСли параметр максимальной цены не передан, то устанавливаем дефолтное
    if max_price is None:
        max_price = MAX_PRICE
    # Если переданы категории предыдущей страницы каталога
    if cat:
        categories = {
            'names': ', '.join(map(lambda x: get(
                f'http://{request.host}/api/categories/{x}'
            ).json()['name'], cat.split(','))),
            'ids': cat
        }
    else:
        categories = {}
    # Получаем список товаров, которые лежат в корзине пользователя,
    # включая количество товаров
    # Получаем список товаров, которые лежат в корзине пользователя,
    # включая количество товаров
    user_basket_info = get(
        f'http://{request.host}/api/user_basket',
        params={'items_list': items_list}
    ).json()
    user_basket = user_basket_info['items']
    total = user_basket_info['total']
    return render_template(
        "item_page.html", title='Продуктовый рай', host_data=request.host,
        item=item, categories=categories, max_price=max_price,
        from_catalog=from_catalog, user_basket=user_basket, total=total
    )


@app.route("/")
def home_page():
    # Проверяем, авторизован ли пользователь, и если да, то получаем список
    # тех товаров, которые он выбрал
    if current_user.is_authenticated:
        # Админ не должен попасть на эту страницу
        if current_user.id == 1:
            abort(404, message=f"No access rights")
        items_list = current_user.items_list
    else:
        items_list = ''
    slides = os.listdir(url_for("static", filename="img/slides")[1:])
    discounted_items = get(
        f'http://{request.host}/api/items', params={'only_discount': True}
    ).json()['items']
    # Получаем список товаров, которые лежат в корзине пользователя,
    # включая количество товаров
    user_basket_info = get(
        f'http://{request.host}/api/user_basket',
        params={'items_list': items_list}
    ).json()
    user_basket = user_basket_info['items']
    total = user_basket_info['total']
    return render_template(
        "index.html", title='Продуктовый рай', host_data=request.host,
        slides=slides, categories=CATEGORIES,
        discounted_items=discounted_items, user_basket=user_basket,
        total=total
    )


@app.route("/personal_account")
def personal_account():
    if current_user.is_authenticated:
        # Админ не должен попасть на эту страницу
        if current_user.id == 1:
            abort(404, message=f"No access rights")
        # Если страница открыта из каталога
        from_catalog = request.args.get('from_catalog')
        # Если открыта страница из товарной страницы
        item_id = request.args.get('from_item_page')
        # Названия фильтров
        cat_filters = request.args.get('cat_filters')
        # id фильтров
        cat_ids = request.args.get('cat')
        # Максимальная цена
        max_price = request.args.get('max_price')
        # Название товара
        item_name = request.args.get('item_name')

        # Получаем все заказы
        orders = get(
            f'http://{request.host}/api/orders',
            params={'user_id': current_user.id}
        ).json()['orders']

        # Еще на каддый товар из списка получаем детальную информацию
        for order in orders:
            order['items_list'] = get(
                f'http://{request.host}/api/user_basket',
                params={'items_list': order['items_list']}
            ).json()['items']

        # Проверяем, авторизован ли пользователь, и если да, то получаем список
        # тех товаров, которые он выбрал
        if current_user.is_authenticated:
            items_list = current_user.items_list
        else:
            items_list = ''
        # Получаем список товаров, которые лежат в корзине пользователя,
        # включая количество товаров
        user_basket_info = get(
            f'http://{request.host}/api/user_basket',
            params={'items_list': items_list}
        ).json()
        user_basket = user_basket_info['items']
        total = user_basket_info['total']

        # Открываем страничку личного кабинета
        return render_template(
            "personal_account.html", title='Продуктовый рай',
            host_data=request.host, orders=orders,
            from_catalog=from_catalog, item_id=item_id,
            cat_filters=cat_filters, cat_ids=cat_ids, item_name=item_name,
            max_price=max_price, user_basket=user_basket, total=total
        )

    # Если пользователь не авторизован, то кидаем ошибку
    abort(404, message=f"User is not authenticated")


@app.route("/add_product", methods=['GET', 'POST'])
def add_product_page():
    """Страничка добавления товара"""

    session = db_session.create_session()
    suppliers_names = [
        supplier.name for supplier in session.query(Supplier).all()
    ]
    categories_names = [
        category.name for category in session.query(Category).all()
    ]

    # создание формы добавления товаров
    form = AddProductForm()
    form.supplier.choices = suppliers_names
    form.category.choices = categories_names

    # Проверка id пользователя (доступ только для id == 1)
    if current_user.is_authenticated and current_user.id == 1:
        # Если нажата кнопка отправки формы
        if form.validate_on_submit():
            session = db_session.create_session()
            # Есть ли наше изображение в переданном запросе
            if 'product_image' in request.files:
                # Загруженное изображение
                image = request.files['product_image']
                if not image.filename:
                    image = Image.open("static/img/default_item_image.png")
                # Проверка формата файла:
                if image.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
                    # Определяем имя файла на основе id последнего товара в бд
                    id_amount = len(session.query(Item.id).all())
                    filename = f"item{id_amount + 1}.png"
                    # Здесь указывается путь до папки на сервере,
                    # где будет сохранен файл
                    path_to_save = os.path.join('./static/img/items',
                                                filename)
                    image.save(path_to_save)
                else:
                    return render_template(
                        'add_product.html', title="Страница управления",
                        form=form, message="Недопустимый формат изображения"
                    )
            # добавляем товар
            post(
                f'http://{request.host}/api/items',
                json={
                    "name": form.name.data,
                    "price": float(form.cost.data),
                    "discount": (
                        int(form.discount.data)
                        if form.discount.data else 0
                    ),
                    "supplier": session.query(Supplier).filter(
                        Supplier.name == form.supplier.data
                    ).first().id,
                    "category": session.query(Category).filter(
                        Category.name == form.category.data
                    ).first().id,
                    "brand": form.brand.data,
                    "type": form.type.data,
                    "type_of_packing": form.type_of_packing.data,
                    "width": form.width.data,
                    "height": form.height.data,
                    "depth": form.depth.data,
                    "weight": form.weight.data,
                    "min_temp": (
                        form.min_temp.data if form.min_temp.data else '0'
                    ),
                    "max_temp": (
                        form.max_temp.data if form.max_temp.data else '0'
                    ),
                    "expiration_date": (
                        f"{form.expiration_date.data} дней"
                        if form.expiration_date.data else 'Не ограничен'
                    ),
                    "calories": form.calories.data,
                    "squirrels": form.squirrels.data,
                    "fats": form.fats.data,
                    "carbohydrates": form.carbohydrates.data,
                    "description": form.extra_information.data,
                    "composition": form.composition.data,
                }
            )
            return redirect('/admin')

        return render_template(
            'add_product.html', title="Добавить товар",
            host_data=request.host, form=form
        )

    abort(404, message=f"No access rights")


@app.route("/update_product/<int:item_id>", methods=['GET', 'POST'])
def update_product_page(item_id):
    """ Редактирование данных о товаре """
    session = db_session.create_session()
    suppliers_names = [
        supplier.name for supplier in session.query(Supplier).all()
    ]
    categories_names = [
        category.name for category in session.query(Category).all()
    ]

    # создание формы добавления товаров
    form = AddProductForm()
    form.supplier.choices = suppliers_names
    form.category.choices = categories_names

    # Подгрузка текущей инфы в поля формочки
    if request.method == "GET":
        # Сессия подключения к БД
        session = db_session.create_session()
        # Достаём товар из БД
        item = session.query(Item).filter(Item.id == item_id).first()
        # Если нашелся
        if item:
            # Заполяняем поле с названием товара
            form.name.data = item.name
            # Заполяняем поле с ценой
            form.cost.data = item.price
            # Заполняем поле со скидкой
            form.discount.data = item.discount
            # Заполняем поле с категориями
            form.category.data = session.query(Category).filter(
                Category.id == item.category
            ).first().name
            # Заполняем поле с поставщиком
            form.supplier.data = session.query(Supplier).filter(
                Supplier.id == item.supplier
            ).first().name
            # Заполняем поле с брендом
            form.brand.data = item.brand
            # Заполняем поле с типом товара
            form.type.data = item.type
            # Заполняем поле с типом упаковки
            form.type_of_packing.data = item.type_of_packing
            # Заполняем поле с шириной
            form.width.data = item.width
            # Заполняем поле с высотой
            form.height.data = item.height
            # Заполняем поле с глубиной
            form.depth.data = item.depth
            # Заполняем поле с весом
            form.weight.data = item.weight
            # Заполняем поле с ёмкостью
            form.capacity.data = item.capacity
            # Заполняем поле с минимальной температурой
            form.min_temp.data = item.min_temp
            # Заполняем поле с максимальной температурой
            form.max_temp.data = item.max_temp
            # Заполняем поле со сроком годности
            form.expiration_date.data = item.expiration_date
            # Заполняем поле с калориями
            form.calories.data = item.calories
            # Заполняем поле с белками
            form.squirrels.data = item.squirrels
            # Заполняем поле с жирами
            form.fats.data = item.fats
            # Заполняем поле с углеводами
            form.carbohydrates.data = item.carbohydrates
            # Заполняем поле с описанием
            form.extra_information.data = item.description
            # Заполняем поле с составом
            form.composition.data = item.composition
        else:
            # Кидаем ошибку
            abort(404)
    # Если пользователь нажал на кнопку
    if form.validate_on_submit():
        # Сессия подключения к БД
        session = db_session.create_session()
        # Достаём товар из БД
        item = session.query(Item).filter(Item.id == item_id).first()
        # Если нашелся
        if item:
            # Есть ли наше изображение в переданном запросе
            if 'product_image' in request.files:
                # Загруженное изображение
                image = request.files['product_image']
                if image.filename:
                    # Проверка формата файла:
                    if image.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
                        # Имя файла
                        filename = f"item{item_id}.png"
                        # Здесь указывается путь до папки на сервере,
                        # где будет сохранен файл
                        path_to_save = os.path.join('./static/img/items',
                                                    filename)
                        image.save(path_to_save)
                    else:
                        return render_template(
                            'add_product.html', title="Страница управления",
                            form=form,
                            message="Недопустимый формат изображения"
                        )
            # Переписываем поле с названием товара
            item.name = form.name.data
            # Переписываем поле с ценой
            item.price = float(form.cost.data)
            # Переписываем поле со скидкой
            item.discount = (
                int(form.discount.data)
                if form.discount.data else 0
            )
            # Переписываем поле с поставщиком
            item.supplier = session.query(Supplier).filter(
                Supplier.name == form.supplier.data
            ).first().id
            # Переписываем поле с категориями
            item.category = session.query(Category).filter(
                Category.name == form.category.data
            ).first().id
            # Переписываем поле с брендом
            item.brand = form.brand.data
            # Переписываем поле с типом товара
            item.type = form.type.data
            # Переписываем поле с типом упаковки
            item.type_of_packing = form.type_of_packing.data
            # Переписываем поле с шириной
            item.width = form.width.data
            # Переписываем поле с высотой
            item.height = form.height.data
            # Переписываем поле с глубиной
            item.depth = form.depth.data
            # Переписываем поле с весом
            item.weight = form.weight.data
            # Переписываем поле с ёмкостью
            item.capacity = form.capacity.data
            # Переписываем поле с минимальной температурой
            item.min_temp = (
                form.min_temp.data if form.min_temp.data else '0'
            )
            # Переписываем поле с максимальной температурой
            item.max_temp = (
                form.max_temp.data if form.max_temp.data else '0'
            )
            # Переписываем поле со сроком годности
            item.expiration_date = (
                f"{form.expiration_date.data} дней"
                if form.expiration_date.data else 'Не ограничен'
            )
            # Переписываем поле с калориями
            item.calories = form.calories.data
            # Переписываем поле с белками
            item.squirrels = form.squirrels.data
            # Переписываем поле с жирами
            item.fats = form.fats.data
            # Переписываем поле с углеводами
            item.carbohydrates = form.carbohydrates.data
            # Переписываем поле с описанием
            item.description = form.extra_information.data
            # Переписываем поле с составом
            item.composition = form.composition.data
            # Коммитим
            session.commit()
            # Перенаправляем в личный кабинет
            return redirect('/admin')
        else:
            # Кидаем ошибку
            abort(404)
    return render_template(
        'add_product.html', title='Редактирование товара',
        host_data=request.host, form=form
    )


@app.route("/add_supplier", methods=['GET', 'POST'])
def add_supplier_page():
    """Страничка добавления товара"""

    # создание формы добавления товаров
    form = AddSupplierForm()

    # Проверка id пользователя (доступ только для id == 1)
    if current_user.is_authenticated and current_user.id == 1:
        # Если нажата кнопка отправки формы
        if form.validate_on_submit():
            # Сессия подключения к БД
            session = db_session.create_session()
            if session.query(Supplier).filter(
                    Supplier.mobile_phone == form.mobile_phone.data
            ).first() or session.query(Supplier).filter(
                Supplier.email == form.email.data
            ).first():
                # Открываем страничку с формой и выводим уведомление о
                # некорректности данных
                return render_template(
                    'add_supplier.html', title="Регистрация поставщика",
                    host_data=request.host, form=form,
                    message="Такой поставщик уже есть"
                )
            # регистрируем поставщика
            post(
                f'http://{request.host}/api/suppliers',
                json={
                    "name": form.name.data,
                    "payment_account": form.payment_account.data,
                    "address": form.payment_account.data,
                    "mobile_phone": form.mobile_phone.data,
                    "email": form.email.data
                }
            )
            return redirect('/admin')

        return render_template(
            'add_supplier.html', title="Регистрация поставщика",
            host_data=request.host, form=form
        )

    abort(404, message=f"No access rights")


@app.route("/update_supplier/<int:supplier_id>", methods=['GET', 'POST'])
def update_supplier_page(supplier_id):
    """ Редактирование данных пользователя """
    form = AddSupplierForm()
    # Подгрузка текущей инфы в поля формочки
    if request.method == "GET":
        # Сессия подключения к БД
        db_sess = db_session.create_session()
        # Достаём нашего пользователя из БД
        supplier = db_sess.query(Supplier).filter(
            Supplier.id == supplier_id
        ).first()
        # Если нашелся
        if supplier:
            # Заполняем поле с именем
            form.name.data = supplier.name
            # Заполняем поле с расчетным счетом
            form.payment_account.data = supplier.payment_account
            # Заполняем поле с адресом
            form.address.data = supplier.address
            # Заполняем поле с мобильным телефоном
            form.mobile_phone.data = supplier.mobile_phone
            # Заполняем поле с электронной почтой
            form.email.data = supplier.email
        else:
            # Кидаем ошибку
            abort(404)
    # Если пользователь нажал на кнопку
    if form.validate_on_submit():
        # Сессия подключения к БД
        db_sess = db_session.create_session()
        # Достаём нашего пользователя из БД
        supplier = db_sess.query(Supplier).filter(
            Supplier.id == supplier_id
        ).first()
        # Если нашелся
        if supplier:
            # Заполняем поле с именем
            supplier.name = form.name.data
            # Заполняем поле с расчетным счетом
            supplier.payment_account = form.payment_account.data
            # Заполняем поле с адресом
            supplier.address = form.address.data
            # Заполняем поле с мобильным телефоном
            supplier.mobile_phone = form.mobile_phone.data
            # Заполняем поле с электронной почтой
            supplier.email = form.email.data
            # Коммитим
            db_sess.commit()
            # Перенаправляем в личный кабинет
            return redirect('/admin')
        else:
            # Кидаем ошибку
            abort(404)
    # Открываем страничку с формочкой
    return render_template(
        'add_supplier.html', title='Редактирование поставщика',
        host_data=request.host, form=form
    )


@app.route("/admin", methods=['GET', 'DELETE', 'POST'])
def admin():
    """Страничка админа"""

    # Проверка id пользователя (доступ только для id == 1)
    if current_user.is_authenticated and current_user.id == 1:
        users = get(f'http://{request.host}/api/users').json()['users']
        items = get(f'http://{request.host}/api/items').json()['items']
        suppliers = get(
            f'http://{request.host}/api/suppliers'
        ).json()['suppliers']

        return render_template(
            'admin.html', title="Админ", host_data=request.host, users=users,
            items=items, suppliers=suppliers
        )

    abort(404, message=f"No access rights")


def main():
    # Устанавливаем соединение с БД
    db_session.global_init(f'db/{DB_NAME}')
    # Запускаем предложение
    app.run()


if __name__ == '__main__':
    main()
