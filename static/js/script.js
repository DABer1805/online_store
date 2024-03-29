// События для слайдера (перемещение мышки: обычное и с зажатой конпкой)
const events = ['mousemove', 'touchmove'];

// Функция, выполняющая GET запрос
async function fetchAsync(url) {
    // Ответ сервера
    let response = await fetch(url);
    // Данные ответа
    let data = await response.json();
    return data;
}

// Добавление товара в корзину
function addItemToBasket(itemId) {
    // ID пользователя
    var userId = document.getElementsByName('current_user')[0].id;
    // Делаем запрос на добавление товара в корзину
    fetchAsync(
        `http://localhost:5000/api/add_item_to_basket/${itemId}/${userId}`
    ).then((result) => {
        // Название товара
        var itemName = result['item']['name'];
        // Цена товара
        var itemPrice = result['item']['price'] * (
            1 - result['item']['discount'] * 0.01
        );
        // Количество товара
        var itemAmount = result['amount'];
        // Обращаемся к контейнеру для сообщений
        var messageContainer = document.getElementById("message_container");
        // Сообщение о добавлении товара в корзину
        var messageDiv = `<div class="alert alert-success" role="alert" \
        id="add_item_message">Товар "${itemName}" добавлен в корзину</div>`;
        // Если в контейнере уже есть сообщение, то удаляем его
        if (messageContainer.querySelector('#add_item_message')) {
            messageContainer.innerHTML = "";
        }
        // Добавляем новое сообщение в контейнер
        messageContainer.insertAdjacentHTML('afterbegin', messageDiv);
        // Если этого товара еще не было в корзине, то добавляем
        // соответсвующую строку в таблицу корзины
        if (itemAmount == 1) {
            // Получение таблицы с корзиной
            var basketTable = document.getElementById(
                "basket_table"
            );
            // Собираем строку таблицы с новым товаром
            var basketRow = `<tr id="item${itemId}_cell" class="noselect"> \
                <td><img src="/static/img/items/item${itemId}.png" \
                 alt="" class="basket_img"></td> \
                <td><a href="#">${itemName}</a></td> \
                <td id="item${itemId}_price">${itemPrice}₽</td> \
                <td id="item${itemId}_total_price"> \
                ${itemPrice * itemAmount}₽</td> \
                <td id="item${itemId}_amount"> \
                <a class="del_amount_btn" id="del_amount${itemId}"> \
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" \
                    height="16" fill="currentColor" class="bi bi-dash" \
                    viewBox="0 0 16 16"> \
                      <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 \
                      1h-7A.5.5 0 0 1 4 8"/> \
                    </svg></a> <span id="amount_container${itemId}" > \
                    ${itemAmount}</span> <a class="add_amount_btn" \
                    id="add_amount${itemId}"> \
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" \
                    height="16" fill="currentColor" class="bi bi-plus" \
                    viewBox="0 0 16 16"> \
                      <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 \
                      1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 \
                      0 0 1 8 4z"/> \
                    </svg> \
                </a> \
                </td> \
            </tr>`
            // Добавляем в таблицу корзины строку с новым товаром
            basketTable.insertAdjacentHTML('beforeend', basketRow);
            // Обращаемся к кнопке добавления товара
            addAmountBtn = document.getElementById(`add_amount${itemId}`)
            // Привязываем функцию добавления товара к этой кнопке
            addAmountBtn.addEventListener('click', function() {
                var itemId = this.id.slice(10);
                addItemToBasket(itemId);
            });
            // Обращаемся к кнопке удаления товара
            delAmountBtn = document.getElementById(`del_amount${itemId}`)
            // Привязываем функцию добавления товара к этой кнопке
            delAmountBtn.addEventListener('click', function() {
                var itemId = this.id.slice(10);
                delItemInBasket(itemId);
            });
        } else {
            // Обращаемся к контейнеру c количеством товара
            var itemAmountContainer = document.getElementById(
                `amount_container${itemId}`
            );
            // Обновляем количество товара
            itemAmountContainer.innerHTML = `${itemAmount}`;

            // Обращаемся к контейнеру
            var itemTotalPriceContainer = document.getElementById(
                `item${itemId}_total_price`
            );
            // Обновляем цену за весь товар
            itemTotalPriceContainer.innerHTML = (
                `${(Math.round(itemPrice * itemAmount * 100) / 100)}₽`
            );
        }
    });
}

function delItemInBasket(itemId) {
    // ID пользователя
    var userId = document.getElementsByName('current_user')[0].id;
    // Делаем звапрос на кдаления товара из корзины
    fetchAsync(
        `http://localhost:5000/api/del_item_in_basket_api/${itemId}/${userId}`
    ).then((result) => {
        // Название товара
        var itemName = result['item']['name'];
        // Если количество товара > 0
        if (result['amount']) {
            // Цена за 1 товар
            var itemPrice = result['item']['price'] * (
                1 - result['item']['discount'] * 0.01
            );
            // Количество товара
            var itemAmount = result['amount'];

            // Обращаемся к контейнеру с количестврм товара
            var itemAmountContainer = document.getElementById(
                `amount_container${itemId}`
            );
            // Обновляем количество товара
            itemAmountContainer.innerHTML = `${itemAmount}`;

            // Обращаемся к контейнеру с ценой за весь товар
            var itemTotalPriceContainer = document.getElementById(
                `item${itemId}_total_price`
            );
            // Обновляем цену за весь товар
            itemTotalPriceContainer.innerHTML = (
                `${(Math.round(itemPrice * itemAmount * 100) / 100)}₽`
            );
        } else {
            // Удаляем строку таблицы с данным товаром
            document.getElementById(`item${itemId}_cell`).remove();
        }
        // Обращаемся к контейнеру для сообщений
        var messageContainer = document.getElementById(
            "message_container"
        );
        // Сообщение об удалении товара из корзины
        var messageDiv = `<div class="alert alert-danger" role="alert" \
        id="add_item_message">Товар "${itemName}" удалён из \
        корзины</div>`;
        // Если в контейнере уже есть сообщение, то удаляем его
        if (messageContainer.querySelector('#add_item_message')) {
            messageContainer.innerHTML = "";
        }
        // Добавляем новое сообщение в контейнер
        messageContainer.insertAdjacentHTML('afterbegin', messageDiv);
    });
}

// Привязываем функцию изменения текущей цены (фильтр) к слайдеру
$.each(events, function(k,v) {
    $('#price_range').on(v, function() {
        $('#price_text').text($('#price_range').val());
    });
})

// Привязываем функцию добавления товара в корзину к соответствующим кнопкам
// (иконка тележки на карточках товаров)
$('.add_item_button').on('click', function() {
    // ID товара
    var itemId = this.id.slice(4);
    // Вызываем функцию добавления товара в корзину
    addItemToBasket(itemId);
});

// Привязываем функцию добавления товара в корзину к соответствующим кнопкам
// (кнопки "+" в интерфейсе корзины)
$('.add_amount_btn').on('click', function() {
    // ID товара
    var itemId = this.id.slice(10);
    // Вызываем функцию добавления товара в корзину
    addItemToBasket(itemId);
});

// Привязываем функцию удаления товара из корзины к соответствующим кнопкам
// (кнопки "-" в интерфейсе корзины)
$('.del_amount_btn').on('click', function() {
    // ID товара
    var itemId = this.id.slice(10);
    // Вызываем функцию удаления товара из корзины
    delItemInBasket(itemId)
});