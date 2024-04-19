import os
import sys

import pytest
from requests import get, post, delete

# Вот тут пришлось вот такими нехорошими вещами заниматься, т.к. при
# запуске из коммандной строки файл не видит папаку data, так что надо
# добавить путь к корневой папке приложения следующими 3-мя строчками
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)

from data.constants import HOST_NAME


# Тесты ресурса с поставщиками

def test_supplier_post_1_correct():
    """ Тестируем post запрос на добавление категории """
    assert post(
        f'http://{HOST_NAME}/api/suppliers',
        json={
            'name': 'Supplier 1',
            'payment_account': '01398745623015069842',
            'address': 'address 1',
            'mobile_phone': '+736502116389',
            'email': 'email1@email.ru'
        }
    ).json() == {'id': 1}


def test_supplier_post_2_correct():
    """ Тестируем post запрос на добавление еще одной категории """
    assert post(
        f'http://{HOST_NAME}/api/suppliers',
        json={
            'name': 'Supplier 2',
            'payment_account': '19478563214569870123',
            'address': 'address 2',
            'mobile_phone': '+71651237896',
            'email': 'email2@email.ru'
        }
    ).json() == {'id': 2}


def test_supplier_get_list():
    """ Тестируем get запрос на получение списка всех поставщиков """
    assert get(f'http://{HOST_NAME}/api/suppliers').json() == {
        'suppliers': [
            {'id': 1, 'mobile_phone': '+736502116389', 'name': 'Supplier 1',
             'payment_account': '01398745623015069842'},
            {'id': 2, 'mobile_phone': '+71651237896', 'name': 'Supplier 2',
             'payment_account': '19478563214569870123'}
        ]
    }


def test_supplier_get_by_id_correct():
    """ Тестируем get запрос на получение одной поставщика по ID, запрос
    корректный (есть поставщик с ID = 1)

    """
    assert get(f'http://{HOST_NAME}/api/suppliers/1').json() == {
        'user': {
            'address': 'address 1',
            'email': 'email1@email.ru',
            'id': 1, 'items': [],
            'mobile_phone': '+736502116389',
            'name': 'Supplier 1',
            'payment_account': '01398745623015069842'
        }
    }


def test_supplier_get_by_id_incorrect():
    """ Тестируем get запрос на получение одного поставщика по ID, запрос
    корректный, но поставщика с таким ID не существует (нет поставщика с
    ID = 999)

    """
    assert get(f'http://{HOST_NAME}/api/suppliers/999').json() == {
        'message': 'Supplier 999 not found'
    }


def test_supplier_delete_by_id_correct():
    """ Тестируем delete запрос на удаление одного поставщика по ID, запрос
    корректный (есть поставщик с ID = 2)

    """
    assert delete(f'http://{HOST_NAME}/api/suppliers/2').json() == {
        'success': 'OK'
    }


def test_supplier_delete_by_id_incorrect():
    """ Тестируем get запрос на получение одного поставщика по ID, запрос
    корректный, но поставщика с таким ID не существует (нет поставщика с
    ID = 999)

    """
    assert delete(f'http://{HOST_NAME}/api/suppliers/999').json() == {
        'message': 'Supplier 999 not found'
    }
