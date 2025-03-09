$(document).ready(function () {
    $('#order_table').DataTable({
        "order": [[0, "desc"]] // Сортировка по ID, в порядке убывания
    })
})

function update_status_order(orderId, status) {
    fetch('/order/action/', {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            'action': 'update_status_order',
            'order_id': orderId,
            'status': status,
        })
    })
        .then(response => response.json())
        .then(data => {
            location.reload();  // Перезагрузить страницу после удаления
        })
        .catch(error => console.error("Ошибка:", error));
}

function delete_order(orderId) {
    if (confirm("Вы уверены, что хотите удалить заказ?")) {
        fetch('/order/action/', {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                'action': 'delete_order',
                'order_id': orderId
            })
        })
            .then(response => response.json())
            .then(data => {
                location.reload();  // Перезагрузить страницу после удаления
            })
            .catch(error => console.error("Ошибка:", error));
    }
}