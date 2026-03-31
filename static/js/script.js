const input = document.getElementById("searchInput");
const select = document.getElementById("categorySelect");

function handleChange() {
const text = input.value;
const category = select.value;
}

input.addEventListener("input", handleChange);
select.addEventListener("change", handleChange);

document.addEventListener('DOMContentLoaded', function() {
    async function load() {
        let url_doctors = `${window.location.href}/api/doctors`;
        let url_occupations = `${window.location.href}/api/occupations`;
        let doctors_json = await (await fetch(url_doctors)).json();
        let occupations_json = await (await fetch(url_occupations)).json();
        for (i in doctors_json)
        {
            console.log(doctors_json[i]["name"]);
            const cards = document.querySelector('.cards');
            const newCard = `
                <div class="card">
                    <img src="https://placehold.co/600x400/EEE/31343C">
                    <div class="container">
                        <p>Ім'я: ${doctors_json[i]["name"]}</p>
                        <p>Спеціальність: ${occupations_json.find(o => o.id === doctors_json[i]["occupation"])?.name}</p>
                        <p>Стаж: ${doctors_json[i]["experience"]}</p>
                        <button class="btn-appointment">Записатися</button>
                    </div>
                </div>
            `;
            cards.innerHTML += newCard;
        }
        occupations_json.forEach(i => {
            const newOption = new Option(i.name, i.id);
            select.add(newOption); 
        });
    }
    load();
});