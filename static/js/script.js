const events = ['mousemove', 'touchmove'];

async function fetchAsync (url) {
    let response = await fetch(url);
    let data = await response.json();
    return data;
}

$.each(events, function(k,v) {
    $('#price_range').on(v, function() {
        $('#price_text').text($('#price_range').val());
    });
})

$('.add_item_button').on('click', function() {
    var item_id = this.id.slice(4);
    fetchAsync(
        `http://localhost:5000/api/add_item_to_basket/${item_id}`
    ).then((result) => {
        var element = document.getElementById("message_container");
        var newElement = `<div class="alert alert-info" role="alert" \
        id="add_item_message">Товар "${result['item']}" \
        добавлен в корзину</div>`;
        if (element.querySelector('#add_item_message')) {
            element.innerHTML = "";
        }
        element.insertAdjacentHTML('afterbegin', newElement);
    });
});