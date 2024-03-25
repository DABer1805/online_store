from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TelField, \
    BooleanField
from wtforms.validators import DataRequired, Length


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
