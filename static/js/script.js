const input = document.getElementById("searchInput");
const select = document.getElementById("categorySelect");

let doctors_json = null;
let occupations_json = null;

function handleChange() {
    const text = input.value;
    const category = select.value;
    console.log(`${text} ${category}`)
    if (doctors_json == null || occupations_json == null){return}
    const cards = document.querySelector('.cards');
    cards.innerHTML = ""
    for (i in doctors_json)
    {
        if (category != 0 && doctors_json[i]["occupation"] != category) { continue }
        if (text != "" && !doctors_json[i]["name"].toLowerCase().includes(text) && !doctors_json[i]["patronym"].toLowerCase().includes(text)) { continue }
        const newCard = `
                <div class="card">
                    <img src="https://placehold.co/600x400/EEE/31343C">
                    <div class="container">
                        <p>Ім'я: ${doctors_json[i]["name"]} ${doctors_json[i]["patronym"]}</p>
                        <p>Спеціальність: ${occupations_json.find(o => o.id === doctors_json[i]["occupation"])?.name}</p>
                        <p>Стаж: ${doctors_json[i]["experience"]} ${getYearAddition(doctors_json[i]["experience"])}</p>
                        <button class="btn-appointment">Записатися</button>
                    </div>
                </div>
            `;
        cards.innerHTML += newCard;
    }

}

input.addEventListener("input", handleChange);
select.addEventListener("change", handleChange);

document.addEventListener('DOMContentLoaded', function() {
    async function load() {
        let url_doctors = `${window.location.href}/api/doctors`;
        let url_occupations = `${window.location.href}/api/occupations`;
        doctors_json = await (await fetch(url_doctors)).json();
        occupations_json = await (await fetch(url_occupations)).json();
        for (i in doctors_json)
        {
            console.log(doctors_json[i]["name"]);
            const cards = document.querySelector('.cards');
            const newCard = `
                <div class="card">
                    <img src="https://placehold.co/600x400/EEE/31343C">
                    <div class="container">
                        <p>Ім'я: ${doctors_json[i]["name"]} ${doctors_json[i]["patronym"]}</p>
                        <p>Спеціальність: ${occupations_json.find(o => o.id === doctors_json[i]["occupation"])?.name}</p>
                        <p>Стаж: ${doctors_json[i]["experience"]} ${getYearAddition(doctors_json[i]["experience"])}</p>
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

function getYearAddition(n) {
  const num = Math.abs(n);
  const lastDigit = num % 10;
  const lastTwoDigits = num % 100;

  if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
    return 'років';
  }
  if (lastDigit === 1) {
    return 'рік';
  }
  if (lastDigit >= 2 && lastDigit <= 4) {
    return 'роки';
  }
  return 'років';
}