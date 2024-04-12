/*
    JS скрипт для интерактивных элементов админской страницы
*/


// Функция переключения вкладок
function switchButton(btnID) {
    // Какая кнопка была нажата
    var someListItemEl = document.getElementById(btnID);
    // Такую вкладку и выбираем
    var tab = new bootstrap.Tab(someListItemEl);

    // Показываем вкладку
    tab.show();
}

// Подвязываем функции переключения вкладок на соответсвующие кнопки
$('#personal-data-btn').on('click', function() {
    switchButton('list-personal-data-list');
});
$('#order-history-btn').on('click', function() {
    switchButton('list-order-history-list');
});
$('#suppliers-btn').on('click', function() {
    switchButton('list-suppliers-list');
});

// Выбираем все кнопочки удаления пользователей
document.querySelectorAll('.delete-user-btn').forEach(button => {
    // И добавляем к ним функции
    button.addEventListener('click', function(e) {
      e.preventDefault();
      // Id пользователя
      var userId = this.dataset.userId;
      // Выводим окно подтверждения
      if (confirm('Вы уверены, что хотите удалить пользователя с ID ' + \
        userId + '?')) {
            // Выполняем кдаление пользоватедя
            fetch('http://localhost:5000/api/users/' + userId, {
              method: 'DELETE',
            }).then(response => {
              if (response.ok) {
                // Если все хорошо
                alert('Пользователь удален');
                window.location.reload();
              }
            }).catch(error => {
                // Что-то поломалось
                alert('Ошибка при удалении пользователя: ' + error);
            });
        }
    });
});

// Выбираем все кнопочки удаления товаров
document.querySelectorAll('.delete-item-btn').forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
        // Id товара
        var itemId = this.dataset.itemId;
        // Выводим окно подтверждения
        if (
            confirm('Вы уверены, что хотите удалить товар с ID ' + itemId + '?')
        ) {
            fetch('http://localhost:5000/api/items/' + itemId, {
              method: 'DELETE',
            }).then(response => {
              if (response.ok) {
                // Если все хорошо
                alert('Товар удален');
                window.location.reload();
           } else {
                     response.json().then(data => {
                        // Что-то поломалось
                       alert('Ошибка при удалении товара: ' + data.message);
                     });
                   }
                 }).catch(error => {
                   // Что-то поломалось
                   alert('Ошибка при удалении товара: ' + error);
                 });
              }
        });
});

document.querySelectorAll('.delete-supplier-btn').forEach(button => {
button.addEventListener('click', function(e) {
        e.preventDefault();
        var supplierId = this.dataset.supplierId;
        // Выводим окно подтверждения
        if (confirm('Вы уверены, что хотите удалить поставщика с ID ' + \
          supplierId + '?')) {
              fetch('http://localhost:5000/api/suppliers/' + supplierId, {
                method: 'DELETE',
              }).then(response => {
                if (response.ok) {
                  // Если все хорошо
                  alert('Поставщик удален');
                  window.location.reload();
                } else {
                  // Что-то поломалось
                  response.json().then(data => {
                    alert(
                      'Ошибка при удалении поставщика: ' + data.message
                    );
                  });
                }
              }).catch(error => {
                // Что-то поломалось
                alert('Ошибка при удалении поставщика: ' + error);
              });
        }
    });
});