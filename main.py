from flask import Flask
from flask_restful import Api

from api import calculate_cost_api
from data.constants import TEST_DB_NAME
from data import db_session
from resources import orders_resources, users_resources, items_resources, \
    categories_resources, suppliers_resources
from data.secret_key import SECRET_KEY

from data.users import User
from forms.user import LoginForm, RegisterForm

from flask_login import LoginManager, login_user, login_required, \
    logout_user

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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("items_list.html", jobs=jobs)


def main():
    db_session.global_init("db/shop.db")
    app.run()


if __name__ == '__main__':
    main()
