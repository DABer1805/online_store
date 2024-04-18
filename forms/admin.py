from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TelField, \
    FileField, FloatField, IntegerField, SelectField, \
    TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, \
    Optional

from data.constants import MAX_PRICE, DB_NAME


class AddProductForm(FlaskForm):
    """Форма добавления продукта"""

    # Загрузка изображения товара
    product_image = FileField(
        'Изображение товара', validators=[Optional()]
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
        'Скидка 0-100%', validators=[Optional(), NumberRange(0, 100)]
    )
    # Категория товара
    category = SelectField(
        'Категория товара',
        validators=[DataRequired()]
    )
    supplier = SelectField(
        'Поставщик',
        validators=[Optional()]
    )
    # Бренд товара
    brand = StringField('Бренд', validators=[Optional()])
    # Тип продукта
    type = StringField('Тип продукта', validators=[Optional()])
    # Тип продукта
    type_of_packing = StringField('Тип упаковки', validators=[Optional()])
    # Ширина
    width = FloatField(
        'Ширина', validators=[Optional(), NumberRange(0, 10000)]
    )
    # Ширина
    height = FloatField(
        'Высота', validators=[Optional(), NumberRange(0, 10000)]
    )
    # Глубина
    depth = FloatField(
        'Глубина', validators=[Optional(), NumberRange(0, 10000)]
    )
    # Вес
    weight = FloatField(
        'Вес', validators=[Optional(), NumberRange(0, 10000)]
    )
    # Емкость
    capacity = FloatField(
        'Емкость', validators=[Optional(), NumberRange(0, 10000)]
    )
    # Минимальная температура
    min_temp = IntegerField(
        'Минимальная температура хранения',
        validators=[Optional(), NumberRange(-100, 100)]
    )
    # Максимальная температура
    max_temp = IntegerField(
        'Максимальная температура хранения',
        validators=[Optional(), NumberRange(-100, 100)]
    )
    # Срок годности
    expiration_date = IntegerField(
        'Срок годности в днях',
        validators=[Optional(), NumberRange(0, 10000000)]
    )
    # Калории
    calories = FloatField(
        'Калории', validators=[Optional(), NumberRange(0, 10000)]
    )
    # Белки
    squirrels = FloatField(
        'Белки', validators=[Optional(), NumberRange(0, 10000)]
    )
    # Жиры
    fats = FloatField(
        'Жиры', validators=[Optional(), NumberRange(0, 10000)]
    )
    # Углеводы
    carbohydrates = FloatField(
        'Углеводы', validators=[Optional(), NumberRange(0, 10000)]
    )
    # Поле дополнительная информация
    extra_information = TextAreaField(
        'Дополнительная информация', validators=[Optional()]
    )
    # Состав
    composition = TextAreaField(
        'Состав', validators=[Optional()]
    )
    # Кнопка отправки формы
    submit = SubmitField('Подтвердить')


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
        'Электронная почта', validators=[DataRequired()]
    )
    # Кнопка отправки формы
    submit = SubmitField('Подтвердить')
