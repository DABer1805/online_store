/*
    JS скрипт для сборки ссылки возвратных кнопок на странице товаров (в
    шаблоне ссылку собирать громоздко сильно) + скрипт для перелистывания
    вкладок: описание, характеристики, состав
*/

// Получаем первую вкладку
var firstTabEl = document.querySelector('#myTab li:last-child a');
var firstTab = new bootstrap.Tab(firstTabEl);

// И показываем её
firstTab.show();

// Id текщего заказа
var itemId = $('#data').data()['itemId'];
// Название товара
var itemName = $('#data').data()['itemName'];
// Фильтр максимальной цены
var maxPrice = $('#data').data()['maxPrice'];
// Названия Категорий - фильтров
var catNames = $('#data').data()['catNames'];
// Id фильтров-категорий
var catIds = $('#data').data()['catIds'];

// Получаем кнопку перехода в личный кабинет
personalAccountLink = document.getElementsByName(
    'current_user'
)[0];
// Собираем ссылку
var link = `${personalAccountLink}?from_catalog=true&from_item_page= \
    ${itemId}&item_name=${itemName}`;
// Если есть фильтр максимальной цены
if (maxPrice) {
    // То добавляем его в ссылку
    link = link + `&max_price=${maxPrice}`;
}
// Если есть фильтры категорий
if (catNames) {
    // То добавляем их в ссылку
    link = link + `&cat_filters=${catNames}`;
    link = link + `&cat=${catIds}`;
}
// Меняем атрибут ссылки у кнопки перехода в личный кабинет
personalAccountLink.setAttribute('href', link);