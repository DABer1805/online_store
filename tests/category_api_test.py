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


# Тесты ресурса с категориями

def test_category_post_1_correct():
    """ Тестируем post запрос на добавление категории """
    assert post(
        f'http://{HOST_NAME}/api/categories',
        json={
            'name': 'Category 1',
        }
    ).json() == {'id': 1}


def test_category_post_2_correct():
    """ Тестируем post запрос на добавление еще одной категории """
    assert post(
        f'http://{HOST_NAME}/api/categories',
        json={
            'name': 'Category 2',
        }
    ).json() == {'id': 2}


def test_category_get_by_id_correct():
    """ Тестируем get запрос на получение однй категории по ID, запрос
    корректный (есть категория с ID = 1)

    """
    assert get(f'http://{HOST_NAME}/api/categories/1').json() == {
        'id': 1, 'items': [], 'name': 'Category 1'
    }


def test_category_get_empty_by_id_incorrect():
    """ Тестируем get запрос на получение однй категории по ID, запрос
    корректный, но категории с таким ID не существует (нет категории с
    ID = 999)

    """
    assert get(f'http://{HOST_NAME}/api/categories/999').json() == {
        'message': 'Category 999 not found'
    }


def test_category_delete_by_id_correct():
    """ Тестируем delete запрос на удаление одной категории по ID, запрос
    корректный (есть категория с ID = 2)

    """
    assert delete(f'http://{HOST_NAME}/api/categories/2').json() == {
        'success': 'OK'
    }


def test_category_delete_empty_by_id_incorrect():
    """ Тестируем get запрос на получение однй категории по ID, запрос
    корректный, но категории с таким ID не существует (нет категории с
    ID = 999)

    """
    assert delete(f'http://{HOST_NAME}/api/categories/999').json() == {
        'message': 'Category 999 not found'
    }
