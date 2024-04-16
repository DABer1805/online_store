/*
    JS скрипт для сборки ссылки возвратных кнопок на странице товаров (в
    шаблоне ссылку собирать громоздко сильно) + скрипт для перелистывания
    вкладок: описание, характеристики, состав
*/

var fromCatalog = $('#data').data()['fromCatalog'];
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
var link = `${personalAccountLink}?from_catalog=true`;
link = link + `&from_item_page=${itemId}&item_name=${itemName}`;
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

var prev_link = '/';

if (fromCatalog != 'None') {
    prev_link = prev_link + `catalog?max_price=${maxPrice}`;

    if (catIds != 'None') {
        prev_link = prev_link + `&cat=${catIds}`;
    }
}

// Стрелочка кнопки возврата
returnToPrevPageBtn = document.getElementById(
    'return_to_prev_page_btn'
);
// Текст кнопки возврата
returnToPrevPageTxt = document.getElementById(
    'return_to_prev_page_txt'
);

// Меняем ссылку у стрелочки возврата на ту, которую ранее собрали
returnToPrevPageBtn.setAttribute('href', prev_link);
// Меняем ссылку у текста возврата на ту, которую ранее собрали
returnToPrevPageTxt.setAttribute('href', prev_link);
// Меняем атрибут ссылки у кнопки перехода в личный кабинет
personalAccountLink.setAttribute('href', link);