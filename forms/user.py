from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TelField, \
    BooleanField, FileField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Email
from data.constants import MAX_PRICE, PRODUCTS_CATEGORIES


class LoginForm(FlaskForm):
    """ Форма авторизации пользователя """
    # Мобильный телефон пользователя
    mobile_phone = TelField(
        'Номер телефона', validators=[DataRequired(), Length(max=15)]
    )
    # Пароль пользователя
    password = PasswordField(
        'Пароль', validators=[DataRequired(), Length(min=5, max=25)]
    )
    # Галочка - "запомнить меня"
    remember_me = BooleanField('Запомнить меня')
    # Кнопка отправки формы
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    """ Форма регистрации пользователя """
    # Мобильный телефон пользователя
    mobile_phone = TelField(
        'Номер телефона', validators=[DataRequired(), Length(max=15)]
    )
    # Пароль пользователя
    password = PasswordField(
        'Пароль', validators=[DataRequired(), Length(min=5, max=25)]
    )
    # Поле для повторного ввода пароля
    password_again = PasswordField(
        'Повторите пароль', validators=[DataRequired(), Length(min=5, max=25)]
    )
    # Фамилия пользователя
    surname = StringField(
        'Фамилия', validators=[DataRequired(), Length(min=1, max=25)]
    )
    # Имя пользователя
    name = StringField(
        'Имя', validators=[DataRequired(), Length(min=1, max=25)]
    )
    # Галочка - "запомнить меня"
    remember_me = BooleanField('Запомнить меня')
    # Кнопка отправки формы
    submit = SubmitField('Войти')


class AddProductForm(FlaskForm):
    """Форма добавления продукта"""

    # Загрузка изображения товара
    product_image = FileField(
        'Изображение товара', validators=[DataRequired()]
    )
    # Имя продукта
    name = StringField('Имя товара', validators=[DataRequired()])
    # Цена
    cost = FloatField(
        'Цена',
        validators=[DataRequired(), NumberRange(1, MAX_PRICE)]
    )
    # Скидка
    discount = IntegerField(
        'Скидка 0-100%', validators=[DataRequired(), NumberRange(0, 100)]
    )
    # Категория товара
    category = SelectField(
        'Категория товара',
        choices=PRODUCTS_CATEGORIES,
        validators=[DataRequired()]
    )
    # Кнопка отправки формы
    submit = SubmitField('Добавить товар')


class AddSupplierForm(FlaskForm):
    """Форма добавления поставщика"""

    # Имя поставщика
    name = StringField('Имя', validators=[DataRequired()])
    # Расчетный счет
    payment_account = IntegerField(
        'Расчетный счет',
        validators=[DataRequired()]
    )
    # Адрес
    address = StringField('Адрес', validators=[DataRequired()])
    # Телефон связи
    mobile_phone = TelField(
        'Номер телефона', validators=[DataRequired(), Length(max=15)]
    )
    # Электронная почта
    email = StringField(
        'Электронная почта', validators=[DataRequired(), Email()]
    )
    # Кнопка отправки формы
    submit = SubmitField('Зарегистрировать')
