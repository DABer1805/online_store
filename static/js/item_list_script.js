/*
    JS скрипт для интерактивных элементов каталога
*/



// События для слайдера (перемещение мышки: обычное и с зажатой конпкой)
const events = ['mousemove', 'touchmove', 'click'];

// Привязываем функцию изменения текущей цены (фильтр) к слайдеру
$.each(events, function(k,v) {
    $('#price_range').on(v, function() {
        $('#price_text').text($('#price_range').val());
    });
})

// Названия фильтров
var catFilters = $('#cat-filters').data()['catFilters'];
// Id фильтров
var catIds = $('#cat-filters').data()['catIds'];
// Получаем Id текущего авторизованного пользователя
personalAccountLink = document.getElementsByName(
    'current_user'
)[0];
// Собираем ссылку
var link = `${personalAccountLink}?from_catalog=true`;

// Если есть фильтры категорий то добавляем их в ссылку
if (catFilters != 'None') {
    link = link + `&cat_filters=${catFilters}&cat=${catIds}`
}
// И меняем атрибут у кнопк иперехода в личный кабинет
personalAccountLink.setAttribute('href', link);

// Текущая страница в каталоге
var curItemListId = 1;

// Функция для замены номера текущей группы товаров нв листалке
function changeCurItemListNumber() {
    // Получаем номер текущей группы
    var curItemListNumber = document.getElementById(
        'cur-item-list-number'
    );
    // Обновляем номер в листалке
    curItemListNumber.innerHTML = `${curItemListId}`;
}

// Перелистывание групп товаров вправо
function toNextItemList() {
    // Получаем текщую группу товров
    var curItemList = document.getElementById(
        `item-list${curItemListId}`
    );
    // И скрываем её
    curItemList.style.display = 'none';

    // Повышаем номер текущей группы товаров на 1
    curItemListId++;
    // Получаем следующую группу товаров
    var nextItemList = document.getElementById(
        `item-list${curItemListId}`
    );
    // И показываем её
    nextItemList.style.display = 'block';

    // Обновляем цифру на листалке
    changeCurItemListNumber(curItemListId);

    // Кнопка "<"
    prevBtn = document.getElementById(
        'item-list-prev-btn-container'
    );

    // Кнопка ">"
    nextBtn = document.getElementById(
        'item-list-next-btn-container'
    );

    // Если это последняя группа товаров, то отруьаем кнопку ">"
    if (nextItemList.getAttribute('name') == 'last') {
        nextBtn.setAttribute(
            'class', 'page-item disabled'
        );
    }
    // И разблокируем кнопку "<"
    prevBtn.setAttribute('class', 'page-item');
}

// Перелистывание групп товаров влево
function toPrevItemList() {
    // Получаем текщую группу товаров
    var curItemList = document.getElementById(
        `item-list${curItemListId}`
    );
    // И прячем её
    curItemList.style.display = 'none';

    // Понижаем номер текщей группы товарров на 1
    curItemListId--;
    var prevItemList = document.getElementById(
        `item-list${curItemListId}`
    );
    // И показываем её
    prevItemList.style.display = 'block';

    // Обновляем цифру на листалке
    changeCurItemListNumber();

    // Кнопка "<"
    prevBtn = document.getElementById(
        'item-list-prev-btn-container'
    );

    // Кнопка ">"
    nextBtn = document.getElementById(
        'item-list-next-btn-container'
    );

    // Если данная группа товаров - первая, то отключаем кнопку "<"
    if (prevItemList.getAttribute('name') == 'first') {
        prevBtn.setAttribute(
            'class', 'page-item disabled'
        );
    }
    // Разблокируем кнопку ">"
    nextBtn.setAttribute('class', 'page-item');
}
// Привязываем функцию перелистывания вправо к кнопке ">"
$('#item-list-next-btn').on('click', function() {
    toNextItemList();
});
// Привязываем функцию перелистывания вправо к кнопке "<"
$('#item-list-prev-btn').on('click', function() {
    toPrevItemList();
});