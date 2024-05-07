function addToOrderList(id, name, price) {
    fetch('/sale/api/cart/', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
        return res.json();
    }).then(function (data) {
        let items = document.getElementsByClassName('cart-counter');
        for (let item of items)
            item.innerText = data.total_quantity;

        location.reload()
    })
}

function updateOrderList(bookId, obj) {
    if (parseInt(obj.value) === 0) {
        if (confirm("Bạn chắc chắn xóa không?") === true) {
            fetch(`/sale/api/cart/${bookId}/`, {
                method: "delete"
            }).then(res => res.json()).then(data => {
                let d = document.getElementsByClassName('cart-counter')
                for (let i = 0; i < d.length; i++)
                    d[i].innerText = data.total_quantity + ' sản phẩm'

                let d2 = document.getElementsByClassName('cart-amount')
                for (let i = 0; i < d2.length; i++)
                    d2[i].innerText = data.total_amount.toLocaleString("en-US") + ' VNĐ'

                let c = document.getElementById(`cart${bookId}`)
                c.style.display = "none"
            }).catch(err => console.info(err)) // promise
        } else {
            obj.value = 1
        }
    } else {
        fetch(`/sale/api/cart/${bookId}/`, {
            method: "put",
            body: JSON.stringify({
                "quantity": obj.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            let d = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity + ' sản phẩm'

            let d2 = document.getElementsByClassName('cart-amount')
            for (let i = 0; i < d2.length; i++)
                d2[i].innerText = data.total_amount.toLocaleString("en-US") + ' VNĐ'
        }).catch(err => console.info(err)) // promise
    }
}

function exportReceipt() {
    // Get form data
    var customer = document.getElementById('customer').value;
    if (customer === '0'){
        alert('Chọn tên người dùng khác');
        return;
    }

    // Encode the data into a query string
    var queryString = "?customer=" + encodeURIComponent(customer);

    // Redirect to the other page with the query string
    window.location.href = "/sale/invoice/export/" + queryString;
}