import pytest

# Подтягиваем тесты api из других файлов
from category_api_test import *
from suppliers_api_test import *
from user_api_test import *
from items_api_test import *

# Главный тестирующий файл, сюда подтягиваются тесты всех остальных api

# ТЕСТЫ ДОЛЖНЫ ИДТИ ИМЕННО В ТАКОМ ПОРЯДКЕ!!!
# ОБЯЗАТЕЛЬНО ЗАПУСКАТЬ С ПУСТОЙ ТЕСТОВОЙ DB!!!
# ОБЯЗАТЕЛЬНО ЗАПУСКАТЬ С ВКЛЮЧЕННЫМ "server.py"!!!
