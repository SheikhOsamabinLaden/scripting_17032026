
let greets_p = document.getElementById("greets");

document.addEventListener('DOMContentLoaded', function() {
    let username = null;
    for (i of document.cookie.split("; "))
    {
        let currCookie = i.split("=");
        if (currCookie[0] == "username")
        {
            username=currCookie[1];
        }
    }
    console.log(username)
    greets_p.innerText = `Вітаємо, ${username}`;
});