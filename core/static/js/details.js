function getCommentBox(c) {
    var name = c.user.name.trim() === '' ? c.user.username : c.user.name;
    return `<li class="list-group-item" style="height: auto">
                <div class="d-flex">
                    <div class="me-2">
                        <img src="${c.user.avatar}" style="height: 75px; width: 75px;"
                                class="rounded-circle" alt="${name}"/>
                    </div>
                    <div class="ms-2 me-2 d-flex align-content-start" style="flex-wrap: wrap">
                        <div class="w-100">
                            <b class="">${name}</b>
                            <small class="text-info">${moment(c.created_date).locale("vi").fromNow()}</small>
                        </div>
                        <div class="m-0 p-0">${c.content}</div>
                    </div>
                </div>
            </li>`;
}

function spinner(status = "block") {
    let s = document.getElementsByClassName("spinner")
    for (let i = 0; i < s.length; i++)
        s[i].style.display = status
}

function loadComments(bookId) {
    spinner();
    fetch(`/api/books/${bookId}/comments/`)
        .then(res => {
            return res.json()
        })
        .then(data => {
            spinner("none")
            let h = "";
            data.forEach(c => {
                h += getCommentBox(c)
            })

            let d = document.getElementById("comments")
            d.innerHTML = h;
        })
}

function addComment(bookId) {
    spinner();
    fetch(`/api/books/${bookId}/comments/`, {
        method: "post",
        body: JSON.stringify({
            "content": document.getElementById("content").value
        }),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    }).then((res) => res.json()).then((data) => {
        spinner("none")
        if (data.status === 204) {
            let c = data.comment
            let h = getCommentBox(c)
            let d = document.getElementById("comments")
            d.innerHTML = h + d.innerHTML;
        } else if (data.status === 501) {
            alert("Bình luận rỗng")
        } else
            alert("Hệ thống bị lỗi!")
    }).catch(err => console.info(err)) // js promise
}