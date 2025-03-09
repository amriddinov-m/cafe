function order_create() {
    let form = document.getElementById("create-order-form");
    let formData = new FormData(form);
    let orderItems = [];

    formData.forEach((value, key) => {
        if (key.startsWith("product_") && parseInt(value) > 0) {
            let productId = key.split("_")[1];
            orderItems.push({
                product_id: productId,
                quantity: parseInt(value)
            });
        }
    });

    if (orderItems.length === 0) {
        alert("Выберите хотя бы одно блюдо.");
        return;
    }

    fetch('/order/action/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")  // CSRF-защита
        },
        body: JSON.stringify({
            items: orderItems,
            'action': 'create_order',
            'table_id': $('#id_select_table').val()
        })
    }).then(response => response.json())
        .then(response => {
            window.location = '/order/list/'
        })
        .catch(error => console.error("Ошибка:", error));
}


