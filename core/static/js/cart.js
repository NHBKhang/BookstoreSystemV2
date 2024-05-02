function addToCart(id, name, price) {
    fetch('/api/cart/', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        }
    }).then(function (res) {
        if (res.ok) {
            return res.json();
        }
        throw new Error('Network response was not ok.');
    }).then(function (data) {
        location.reload();

        let items = document.getElementsByClassName('cart-counter');
        for (let item of items)
            item.innerText = data.total_quantity;

        let d2 = document.getElementsByClassName('cart-amount')
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString("en-US") + ' VNĐ'
    })
}

function updateCart(bookId, obj) {
    fetch(`/api/cart/${bookId}/`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie('csrftoken')
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementsByClassName('cart-amount')
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString("en-US") + ' VNĐ'

        location.reload()
    }).catch(err => console.info(err)) // promise
}

function deleteCart(bookId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/api/cart/${bookId}/`, {
            method: "delete",
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        }).then(res => res.json()).then(data => {
            let d = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let d2 = document.getElementsByClassName('cart-amount')
            for (let i = 0; i < d2.length; i++)
                d2[i].innerText = data.total_amount.toLocaleString("en-US")

            let c = document.getElementById(`cart${bookId}`)
            c.style.display = "none"
        }).catch(err => console.info(err)) // promise
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}