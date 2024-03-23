import pytest
from requests import get, post, delete


# Тесты ресурса с товарами

def test_item_get_empty():
    """ Тестируем get запрос на получение одного товара -
    таблица товаров пустая

    """
    assert get('http://localhost:5000/api/items').json() == {'items': []}


def test_item_post_1_correct():
    """ Тестируем get запрос на получение одного товара -
    таблица товаров пустая

    """
    assert post(
        'http://localhost:5000/api/items',
        json={
            'name': 'Item 1',
            'price': 125,
            'discount': 20,
            'supplier': 1,
            'category': 1
        }
    ).json() == {'id': 1}


def test_item_get_by_id_correct():
    """ Тестируем get запрос на получение одного товара -
    в таблице есть товар - со следующими полями с ID = 1

    """
    assert get('http://localhost:5000/api/items/1').json() == {
        'item': {
            'category': 1, 'discount': 20,
            'name': 'Item 1', 'price': 125,
            'supplier': 1
        }
    }


def test_item_post_2_correct():
    """ Тестируем get запрос на получение одного товара -
    таблица товаров пустая

    """
    assert post(
        'http://localhost:5000/api/items',
        json={
            'name': 'Item 2',
            'price': 145,
            'discount': 50,
            'supplier': 1,
            'category': 1
        }
    ).json() == {'id': 2}


def test_item_get_list():
    """ Тестируем get запрос на получение одного товара -
    таблица товаров пустая

    """
    assert get('http://localhost:5000/api/items').json() == {
        'items': [{'discount': 20, 'name': 'Item 1', 'price': 125},
                  {'discount': 50, 'name': 'Item 2', 'price': 145}]
    }


def test_delete_item_by_id_correct():
    """ Тестируем get запрос на получение одного товара -
    таблица товаров пустая

    """
    assert delete('http://localhost:5000/api/items/2').json() == {
        'success': 'OK'
    }
