# Реальная БД
DB_NAME = 'shop.db'
# БД для тестов (если вдруг добавляется новый функционал к api)
TEST_DB_NAME = 'shop_test.db'
# Максимальная цена товара (для слайдера на экране фильтрации)
MAX_PRICE = 10000
# Доступные расширения для изображений товара
ALLOWED_EXTENSIONS = ('png', )
# Категории товаров на карточках главной страницы
CATEGORIES = [
    {'name': 'Все товары', 'link': f'/catalog?max_price={MAX_PRICE}'},
    {'name': 'Овощи и фрукты',
     'link': f'/catalog?cat=3&max_price={MAX_PRICE}'},
    {'name': 'Молоко, сыр, яйца',
     'link': f'/catalog?cat=1,2&max_price={MAX_PRICE}'},
    {'name': 'Мясо, птица, колбасы',
     'link': f'/catalog?cat=4,9&max_price={MAX_PRICE}'},
    {'name': 'Хлеб, выпечка, снеки',
     'link': f'/catalog?cat=6&max_price={MAX_PRICE}'},
    {'name': 'Рыба и морепродукты',
     'link': f'/catalog?cat=10&max_price={MAX_PRICE}'}
]
# Во время запуска тестов нужно здесь указать адрес хоста, т.к. файлы с
# тестами обрабатываются отдельно от сервера и там нельзя получить хоста с
# помощью request.host
HOST_NAME = '127.0.0.1:5000'