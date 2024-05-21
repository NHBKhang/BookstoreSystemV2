function reorder(order_id) {
    fetch(`/reorder/${order_id}/`, {
        method: 'post',
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    }).then(res => {

    }).catch(ex => {

    })
}