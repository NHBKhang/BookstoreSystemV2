window.onscroll = function () {
    let r = document.getElementById("return")
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        r.style.display = "block";
    } else {
        r.style.display = "none";
    }
}

function scrollToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function showPassword(e, nameId = 'password') {
    var input = document.getElementById(nameId)
    if (input.type === 'password') {
        input.type = "text"
        e.target.className = "fas fa-eye"
    } else {
        input.type = "password"
        e.target.className = "fas fa-eye-slash"
    }
}