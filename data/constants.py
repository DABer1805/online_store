# Реальная БД
DB_NAME = 'shop.db'
# БД для тестов (если вдруг добавляется новый функционал к api)
TEST_DB_NAME = 'shop_test.db'
# Максимальная цена товара (для слайдера на экране фильтрации)
MAX_PRICE = 10000
CATEGORIES = [
    {'name': 'Все товары', 'link': '/catalog'},
    {'name': 'Овощи и фрукты', 'link': '/catalog?cat=3'},
    {'name': 'Молоко, сыр, яйца', 'link': '/catalog?cat=1,2'},
    {'name': 'Мясо, птица, колбасы', 'link': '/catalog?cat=4,9'},
    {'name': 'Хлеб, выпечка, снеки', 'link': '/catalog?cat=6'},
    {'name': 'Рыба и морепродукты', 'link': '/catalog?cat=10'}
]
