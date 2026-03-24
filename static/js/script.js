document.addEventListener('DOMContentLoaded', function() {
    async function load() {
        let url = `${window.location.href}/api/doctors`;
        let obj = await (await fetch(url)).json();
        for (i in obj)
        {
            console.log(obj[i]["name"]);
            const cards = document.querySelector('.cards');
            const newCard = `
                <div class="card">
                    <img src="https://placehold.co/600x400/EEE/31343C">
                    <div class="container">
                        <p>Ім'я: ${obj[i]["name"]}</p>
                        <p>Спеціальність: ${obj[i]["occupation"]}</p>
                        <p>Стаж: ${obj[i]["experience"]}</p>
                        <button class="btn-appointment">Записатися</button>
                    </div>
                </div>
            `;
            cards.innerHTML += newCard;
        }

    }
    load();
});