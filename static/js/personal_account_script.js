/*
    JS скрипт для динамических элементов в личном кабинете
*/


// Ссылка для возврата на предыдущую страничку
var link = '/';

// Id товара
var itemId = $('#data').data()['itemId'];
// Максимальная цена
var maxPrice = $('#data').data()['maxPrice'];
// Id фильтров
var catIds = $('#data').data()['catIds'];
// Открыто ли из каталога
var fromCatalog = $('#data').data()['fromCatalog'];

// Если открыто из каталога
if (fromCatalog != 'None') {
    // Добавляем это каталог в ссылку
    link = link + 'catalog';
    // Если есть Id товара - то открыто из странички о товаре
    if (itemId != 'None') {
        // Добавляем это в ссылку
        link = link + `/${itemId}`;
        // Если указан фильтр цены, то добавляем в ссылку
        if (maxPrice != 'None') {
            link = link + `?max_price=${maxPrice}`;
        }
        // И добавляем в конец Id товара
        link = link + '&from_item_page=${itemId}';
    }
    // Фильтр цены и чисто каталог
    if (maxPrice != 'None') {
        link = link + `?max_price=${maxPrice}`;
    }
    // Фильтры категорий и чисто каталог
    if (catIds != 'None') {
        link = link + `&cat=${catIds}`;
    }
    // Доавляем маркер, что открыто из каталога
    link = link + '&from_catalog=true';
}

// Стрелочка кнопки возврата
returnToPrevPageBtn = document.getElementById(
    'return_to_prev_page_btn'
);
// Текст кнопки возврата
returnToPrevPageTxt = document.getElementById(
    'return_to_prev_page_txt'
);
// Бредкрамб со страничкой о товаре
itemPageHref = document.getElementById(
    'item-page-href'
);

// Меняем ссылку у стрелочки возврата на ту, которую ранее собрали
returnToPrevPageBtn.setAttribute('href', link);
// Меняем ссылку у текста возврата на ту, которую ранее собрали
returnToPrevPageTxt.setAttribute('href', link);
// Меняем ссылку у бредкрамба странички о товаре на ту, которую ранее
// собрали (если имеется бредкрамб)
if (itemPageHref) {
    itemPageHref.setAttribute('href', link);
}

// Номер текущего заказа
var curOrderId = 1;

// Функция переключения вкладок
function switchButton(btnID) {
    // Какая кнопка была нажата
    var someListItemEl = document.getElementById(btnID);
    // Такую вкладку и выбираем
    var tab = new bootstrap.Tab(someListItemEl);

    // Показываем вкладку
    tab.show();
}

function changeCurOrderNumber() {
    // Берем окошечко с номером текущего заказа
    var curOrderNumber = document.getElementById(
        'cur-order-number'
    );
    // И обновляем там цифорку
    curOrderNumber.innerHTML = `${curOrderId}`;
}

// Перелистывание табличек с заказами вправо
function toNextOrder() {
    // Текущая табличка с заказом
    var curOrder = document.getElementById(
        `order${curOrderId}`
    );
    // Прячем её
    curOrder.style.display = 'none';

    // Прибавляем номер текущего заказа на 1
    curOrderId++;
    // Берем следующую табличку
    var nextOrder = document.getElementById(
        `order${curOrderId}`
    );
    // И открываем её
    nextOrder.style.display = 'block';

    // Обновляем цифру на листалке
    changeCurOrderNumber();

    // Кнопка перелистывания влево
    prevBtn = document.getElementById(
        'order-prev-btn-container'
    );

    // Кнопка перелистывания вправо
    nextBtn = document.getElementById(
        'order-next-btn-container'
    );

    // Если табличка - последняя, то прячем кнопку перелистывания вправо
    if (nextOrder.getAttribute('name') == 'last') {
        nextBtn.setAttribute(
            'class', 'page-item disabled'
        );
    }
    // Разблокируем кнопку перелистывания влево
    prevBtn.setAttribute('class', 'page-item');
}

// Перелистывание табличек с заказами влево
function toPrevOrder() {
    // Текущая табличка с заказом
    var curOrder = document.getElementById(
        `order${curOrderId}`
    );
    // Прячем её
    curOrder.style.display = 'none';

    // Уменьшаем номер текущего заказа на 1
    curOrderId--;
    // Табличка с предыдущим заказом
    var prevOrder = document.getElementById(
        `order${curOrderId}`
    );
    // Открываем её
    prevOrder.style.display = 'block';

     // Обновляем цифру на листалке
    changeCurOrderNumber(curOrderId);

    // Кнопка перелистывания влево
    prevBtn = document.getElementById(
        'order-prev-btn-container'
    );

    // Кнопка перелистывания вправо
    nextBtn = document.getElementById(
        'order-next-btn-container'
    );

    // Если табличка - певрая, то прячем кнопку перелистывания влево
    if (prevOrder.getAttribute('name') == 'first') {
        prevBtn.setAttribute(
            'class', 'page-item disabled'
        );
    }
    // Открываем кнопку перелистывания вправо
    nextBtn.setAttribute('class', 'page-item');
}

// Подкрепляем функцию переличтывания к переключателям вкладок
$('#personal-account-btn').on('click', function() {
    switchButton('list-personal-account-list');
});
$('#personal-data-btn').on('click', function() {
    switchButton('list-personal-data-list');
});
$('#order-history-btn').on('click', function() {
    switchButton('list-order-history-list');
});
// Подкрепляем функцию перелистывания влево для кнопки '<'
$('#order-next-btn').on('click', function() {
    toNextOrder();
});
// Подкрепляем функцию перелистывания вправо для кнопки '>'
$('#order-prev-btn').on('click', function() {
    toPrevOrder();
});