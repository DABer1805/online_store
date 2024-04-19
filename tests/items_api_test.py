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


# Тесты ресурса с товарами

def test_item_get_empty():
    """ Тестируем get запрос на получение одного товара -
    таблица товаров пустая

    """
    assert get(f'http://{HOST_NAME}/api/items').json() == {'items': []}


def test_item_post_1_correct():
    """ Тестируем get запрос на получение одного товара -
    таблица товаров пустая

    """
    assert post(
        f'http://{HOST_NAME}/api/items',
        json={
            'name': 'Item 1',
            'price': 125,
            'discount': 20,
            'supplier': 1,
            'category': 1,
            'brand': 'brand',
            'type': 'type',
            'type_of_packing': 'type_of_packing',
            'width': '0',
            'height': '0',
            'depth': '0',
            'weight': '0',
            'capacity': '0',
            'min_temp': '0',
            'max_temp': '0',
            'expiration_date': '',
            'calories': '0',
            'squirrels': '0',
            'fats': '0',
            'carbohydrates': '0',
            'description': 'description',
            'composition': 'composition'
        }
    ).json() == {'id': 1}


def test_item_get_by_id_correct():
    """ Тестируем get запрос на получение одного товара -
    в таблице есть товар - со следующими полями с ID = 1

    """
    assert get(f'http://{HOST_NAME}/api/items/1').json() == {
        'item': {
            'brand': 'brand', 'calories': '0', 'capacity': '0',
            'carbohydrates': '0', 'category': 1,
            'composition': 'composition', 'depth': '0',
            'description': 'description', 'discount': 20.0,
            'expiration_date': '', 'fats': '0', 'height': '0', 'id': 1,
            'max_temp': '0', 'min_temp': '0', 'name': 'Item 1',
            'price': 125.0, 'squirrels': '0', 'supplier': 'Supplier 1',
            'type': 'type', 'type_of_packing': 'type_of_packing',
            'weight': '0', 'width': '0'
        }
    }


def test_item_post_2_correct():
    """ Тестируем get запрос на получение одного товара -
    таблица товаров пустая

    """
    assert post(
        f'http://{HOST_NAME}/api/items',
        json={
            'name': 'Item 2',
            'price': 145,
            'discount': 50,
            'supplier': 1,
            'category': 1,
            'brand': 'brand',
            'type': 'type',
            'type_of_packing': 'type_of_packing',
            'width': '0',
            'height': '0',
            'depth': '0',
            'weight': '0',
            'capacity': '0',
            'min_temp': '0',
            'max_temp': '0',
            'expiration_date': '',
            'calories': '0',
            'squirrels': '0',
            'fats': '0',
            'carbohydrates': '0',
            'description': 'description',
            'composition': 'composition'
        }
    ).json() == {'id': 2}


def test_item_get_list():
    """ Тестируем get запрос на получение нескольких товаров -
    таблица товаров пустая

    """
    assert get(f'http://{HOST_NAME}/api/items').json() == {
        'items': [
            {'discount': 20.0, 'id': 1, 'name': 'Item 1', 'price': 125.0},
            {'discount': 50.0, 'id': 2, 'name': 'Item 2', 'price': 145.0}
        ]}



def test_delete_item_by_id_incorrect():
    """ Тестируем get запрос на получение одного поставщика по ID, запрос
    корректный, но поставщика с таким ID не существует (нет поставщика с
    ID = 999)

    """
    assert delete(f'http://{HOST_NAME}/api/items/999').json() == {
        'message': 'Item 999 not found'
    }
