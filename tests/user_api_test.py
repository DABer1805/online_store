import pytest

from requests import get, post, delete

import sys
import os

# Вот тут пришлось вот такими нехорошими вещами заниматься, т.к. при
# запуске из коммандной строки файл не видит папаку data, так что надо
# добавить путь к корневой папке приложения следующими 3-мя строчками
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)

from data.constants import TEST_DB_NAME
from data import db_session
from data.users import User


# Тесты ресурса с пользователями

def test_user_post_1_correct():
    """ Тестируем post запрос на добавление пользователя """
    assert post(
        'http://localhost:5000/api/users',
        json={
            'name': 'User 1 name',
            'surname': 'User 1 surname',
            'items_list': '1x4',
            'mobile_phone': '+736502116389',
        }
    ).json() == {'id': 1}


def test_user_post_2_correct():
    """ Тестируем post запрос на добавление еще одного пользователя """
    assert post(
        'http://localhost:5000/api/users',
        json={
            'name': 'User 2 name',
            'surname': 'User 2 surname',
            'items_list': '1x15',
            'mobile_phone': '+71651237896',
        }
    ).json() == {'id': 2}


def test_user_get_list():
    """ Тестируем get запрос на получение списка всех пользователей """
    assert get('http://localhost:5000/api/users').json() == {
        'users': [
            {
                'id': 1, 'items_list': '1x4',
                'mobile_phone': '+736502116389', 'name': 'User 1 name',
                'surname': 'User 1 surname'
            },
            {
                'id': 2, 'items_list': '1x15',
                'mobile_phone': '+71651237896', 'name': 'User 2 name',
                'surname': 'User 2 surname'
            }
        ]
    }



def test_user_get_by_id_correct():
    """ Тестируем get запрос на получение одной пользователя по ID, запрос
    корректный (есть пользователя с ID = 1)

    """
    assert get('http://localhost:5000/api/users/1').json() == {
        'user': {
            'id': 1, 'items_list': '1x4', 'mobile_phone': '+736502116389',
            'name': 'User 1 name', 'surname': 'User 1 surname'
        }
    }



def test_user_get_by_id_incorrect():
    """ Тестируем get запрос на получение одного пользователя по ID, запрос
    корректный, но пользователя с таким ID не существует (нет пользователя с
    ID = 999)

    """
    assert get('http://localhost:5000/api/users/999').json() == {
        'message': 'User 999 not found'
    }


def test_user_delete_by_id_correct():
    """ Тестируем delete запрос на удаление одного пользователя по ID,
    запрос
    корректный (есть пользователя с ID = 2)

    """
    assert delete('http://localhost:5000/api/users/2').json() == {
        'success': 'OK'
    }


def test_user_delete_by_id_incorrect():
    """ Тестируем get запрос на получение одного пользователя по ID, запрос
    корректный, но пользователя с таким ID не существует (нет пользователя с
    ID = 999)

    """
    assert delete('http://localhost:5000/api/users/999').json() == {
        'message': 'User 999 not found'
    }


def test_user_set_password():
    """ Тестируем установку хэшированного пароля пользователю """
    db_session.global_init(f'db/{TEST_DB_NAME}')
    session = db_session.create_session()
    user = session.query(User).first()
    user.set_password('qwerty12345')
    session.commit()
    assert user.hashed_password is not None


def test_user_check_password():
    """ Тестируем проверку пароля пользователю """
    db_session.global_init(f'db/{TEST_DB_NAME}')
    session = db_session.create_session()
    user = session.query(User).first()
    assert user.check_password('qwerty12345') is True
