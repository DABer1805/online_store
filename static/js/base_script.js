/*
    JS скрипт для всего, что связано с базовым шаблоном и добавлением товаров
    (механизм работы карточек пи корзины связаны друг с другом, да и карточки
    не только в каталоге используются
*/

// Адрес сервера
var hostLink = $('#host-data').data()['host'];


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
        `http://${hostLink}/api/add_item_to_basket/${itemId}/${userId}`
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
        var messageDiv = `<div class="alert alert-success alert-dismissible
        fade show" role="alert" id="add_item_message">Товар "${itemName}"
        добавлен в корзину<button type="button" class="btn-close"
        data-bs-dismiss="alert" aria-label="Close"></button></div>`;
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
            var basketRow = `<tr id="item${itemId}_cell" class="noselect">
                <td><img src="/static/img/items/item${itemId}.png"
                 alt="" class="basket_img"></td>
                <td>${itemName}</td>
                <td id="item${itemId}_price">
                ${(Math.round(itemPrice * 100) / 100)}₽</td>
                <td id="item${itemId}_total_price">
                ${(Math.round(itemPrice * itemAmount * 100) / 100)}₽</td>
                <td id="item${itemId}_amount">
                <a class="del_amount_btn" id="del_amount${itemId}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16"
                    height="16" fill="currentColor" class="bi bi-dash"
                    viewBox="0 0 16 16">
                      <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0
                      1h-7A.5.5 0 0 1 4 8"/>
                    </svg></a> <span id="amount_container${itemId}" >
                    ${itemAmount}</span> <a class="add_amount_btn"
                    id="add_amount${itemId}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16"
                    height="16" fill="currentColor" class="bi bi-plus"
                    viewBox="0 0 16 16">
                      <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0
                      1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5
                      0 0 1 8 4z"/>
                    </svg>
                </a>
                </td>
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

        // Ячейка с итоговой ценой заказа
        totalCell = document.getElementById('total-cell');

        // Получаем эту цену
        total = parseFloat(totalCell.innerHTML.slice(7, -1));
        // Прибавляем туда цену товара
        total = (Math.round((total + itemPrice) * 100) / 100);

        // И перезаписываем итоговую цену
        totalCell.innerHTML = `Итого: ${total}₽`;
    });
}

// Удаление товара из корзины
function delItemInBasket(itemId) {
    // ID пользователя
    var userId = document.getElementsByName('current_user')[0].id;
    // Делаем звапрос на кдаления товара из корзины
    fetchAsync(
        `http://${hostLink}/api/del_item_in_basket_api/${itemId}/${userId}`
    ).then((result) => {
        // Название товара
        var itemName = result['item']['name'];
        // Цена за 1 товар
        var itemPrice = result['item']['price'] * (
            1 - result['item']['discount'] * 0.01
        );
        // Если количество товара > 0
        if (result['amount']) {
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
        // Ячейка с итоговой ценой заказа
        totalCell = document.getElementById('total-cell');

        // Получаем эту цену
        total = parseFloat(totalCell.innerHTML.slice(7, -1));
        // Отнимаем там цену товара
        total = (Math.round((total - itemPrice) * 100) / 100);

        // И перезаписываем итоговую цену
        totalCell.innerHTML = `Итого: ${total}₽`;

        // Обращаемся к контейнеру для сообщений
        var messageContainer = document.getElementById(
            "message_container"
        );
        // Сообщение об удалении товара из корзины
        var messageDiv = `<div class="alert alert-danger alert-dismissible
        fade show" role="alert" id="add_item_message">Товар "${itemName}"
        удалён из корзины<button type="button" class="btn-close"
        data-bs-dismiss="alert" aria-label="Close"></button></div>`;
        // Если в контейнере уже есть сообщение, то удаляем его
        if (messageContainer.querySelector('#add_item_message')) {
            messageContainer.innerHTML = "";
        }
        // Добавляем новое сообщение в контейнер
        messageContainer.insertAdjacentHTML('afterbegin', messageDiv);
    });
}

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

// Привязываем функцию добавления товара в корзину к соответствующим кнопкам
// (кнопки "-" в интерфейсе корзины)
$('.del_amount_btn').on('click', function() {
    // ID товара
    var itemId = this.id.slice(10);
    // Вызываем функцию добавления товара в корзину
    delItemInBasket(itemId);
});

// Привязываем функцию формирования заказа
$('#make_order_btn').on('click', function() {
    // ID пользователя
    var userId = document.getElementsByName('current_user')[0].id;
    // Выполняем запрос на формирование заказа
    fetchAsync(
        `http://${hostLink}/api/make_order/${userId}`
    ).then((result) => {;
        if (result['status'] == 'OK') {
            // Сообщение о выполнении заказа
            var messageDiv = `<tr><td class="table-success" role="alert"
            id="add_item_message"  colspan="5">Заказ успешно выполнен
            </td></tr>`;
        } else {
            // Сообщение о пустой корзине
            var messageDiv = `<tr><td class="table-danger" role="alert"
            id="add_item_message"  colspan="5">Корзина пуста!!!
            </td></tr>`;
        }
        // Ячейка с итоговой ценой заказа
        totalCell = document.getElementById('total-cell');
        // И перезаписываем итоговую цену
        totalCell.innerHTML = 'Итого: 0₽';

        basketTable = document.getElementById('basket_table');
        basketTable.innerHTML = messageDiv;
    })
});