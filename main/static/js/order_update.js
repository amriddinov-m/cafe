function order_update(orderId) {

    let form = document.getElementById("update-order-form");
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
    console.log(orderItems)

    if (orderItems.length === 0) {
        alert("Выберите хотя бы одно блюдо.");
        return;
    }

    fetch("/order/action/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            items: orderItems,
            'action': 'update_order',
            'table_id': $('#id_select_table').val(),
            'order_id': `${orderId}`,
        })
    }).then(response => response.json())
        .then(response => {
            console.log(response)
            window.location = '/order/list/'
        })
        .catch(error => console.error("Ошибка:", error));
}