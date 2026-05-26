const input = document.getElementById("searchInput");
const select = document.getElementById("categorySelect");

let doctors_json = null;
let occupations_json = null;

function getYearAddition(n) {
    const num = Math.abs(parseInt(n) || 0); 
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

function handleChange() {
    const text = input.value.toLowerCase();
    const category = select.value;
    
    if (doctors_json == null || occupations_json == null){return}
    const cards = document.querySelector('.cards');
    cards.innerHTML = "";
    
    for (let i in doctors_json) {
        if (category != 0 && doctors_json[i]["occupation"] != category) { continue }
        if (text != "" && !doctors_json[i]["name"].toLowerCase().includes(text) && !doctors_json[i]["patronym"].toLowerCase().includes(text)) { continue }
        
        let doctorNameStr = `${doctors_json[i]["name"]} ${doctors_json[i]["patronym"]}`;
        let expNumber = parseInt(doctors_json[i]["experience"]); 
        
        const newCard = `
            <div class="card">
                <img src="https://placehold.co/600x400/EEE/31343C">
                <div class="container">
                    <p>Ім'я: ${doctorNameStr}</p>
                    <p>Спеціальність: ${occupations_json.find(o => o.id === doctors_json[i]["occupation"])?.name}</p>
                    <p>Стаж: ${expNumber} ${getYearAddition(expNumber)}</p>
                    <button class="btn-appointment" onclick="openSchedule(${doctors_json[i]["id"]}, '${doctorNameStr}')">Записатися</button>
                </div>
            </div>
        `;
        cards.innerHTML += newCard;
    }
}

input.addEventListener("input", handleChange);
select.addEventListener("change", handleChange);

document.addEventListener('DOMContentLoaded', async function() {
    let url_doctors = `/api/doctors`;
    let url_occupations = `/api/occupations`;
    
    doctors_json = await (await fetch(url_doctors)).json();
    occupations_json = await (await fetch(url_occupations)).json();
    
    const cards = document.querySelector('.cards');
    for (let i in doctors_json) {
        let doctorNameStr = `${doctors_json[i]["name"]} ${doctors_json[i]["patronym"]}`;
        let expNumber = parseInt(doctors_json[i]["experience"]); 
        
        const newCard = `
            <div class="card">
                <img src="https://placehold.co/600x400/EEE/31343C">
                <div class="container">
                    <p>Ім'я: ${doctorNameStr}</p>
                    <p>Спеціальність: ${occupations_json.find(o => o.id === doctors_json[i]["occupation"])?.name}</p>
                    <p>Стаж: ${expNumber} ${getYearAddition(expNumber)}</p>
                    <button class="btn-appointment" onclick="openSchedule(${doctors_json[i]["id"]}, '${doctorNameStr}')">Записатися</button>
                </div>
            </div>
        `;
        cards.innerHTML += newCard;
    }
    
    occupations_json.forEach(i => {
        const newOption = new Option(i.name, i.id);
        select.add(newOption); 
    });

    const modal = document.getElementById("appointmentModal");
    const closeBtn = document.querySelector(".close-btn");
    
    closeBtn.onclick = function() {
        modal.style.display = "none";
    }
    
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});

window.openSchedule = async function(doctorId, doctorName) {
    if (!IS_LOGGED_IN) {
        alert("Для запису потрібно увійти в систему!");
        window.location.href = "/login";
        return;
    }

    const modal = document.getElementById("appointmentModal");
    document.getElementById("modalDoctorName").innerText = doctorName;
    modal.style.display = "block";
    
    const container = document.getElementById("scheduleContainer");
    container.innerHTML = "<p>Завантаження розкладу...</p>";
    

    let res = await fetch(`/api/appointments/doctor/${doctorId}`);
    let bookedSlotsRaw = await res.json();
    

    let bookedSlots = bookedSlotsRaw.map(slot => slot.substring(0, 16));
    
    generateSchedule(doctorId, bookedSlots);
}


function generateSchedule(doctorId, bookedSlots) {
    const container = document.getElementById("scheduleContainer");
    container.innerHTML = "";
    
    let now = new Date();
    
    for(let d = 1; d <= 7; d++) { 
        let currentDay = new Date();
        currentDay.setDate(now.getDate() + d);
        
        let dateString = currentDay.toISOString().split('T')[0];
        
        let dayDiv = document.createElement("div");
        dayDiv.className = "schedule-day";
        dayDiv.innerHTML = `<h3>${currentDay.toLocaleDateString('uk-UA', { weekday: 'long', day: 'numeric', month: 'long'})}</h3>`;
        
        let slotsDiv = document.createElement("div");
        slotsDiv.className = "slots-grid";
        
        for(let h = 9; h <= 16; h++) {
            for(let m of ['00', '30']) {
                let timeString = `${h.toString().padStart(2, '0')}:${m}`;
                

                let compareString = `${dateString}T${timeString}`; 

                let fullDateTime = `${compareString}:00`; 
                
                let btn = document.createElement("button");
                btn.className = "time-slot";
                btn.innerText = timeString;
                
                if(bookedSlots.includes(compareString)) {
                    btn.disabled = true;
                    btn.classList.add("booked");
                } else {
                    btn.onclick = () => bookAppointment(doctorId, fullDateTime);
                }
                slotsDiv.appendChild(btn);
            }
        }
        dayDiv.appendChild(slotsDiv);
        container.appendChild(dayDiv);
    }
}


window.bookAppointment = async function(doctorId, dateTimeString) {
    if (confirm(`Підтверджуєте запис на ${dateTimeString.replace('T', ' ')}?`)) {
        let res = await fetch("/api/appointments", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                doctor_id: doctorId,
                time: dateTimeString
            })
        });
        
        if (res.ok) {
            alert("Ви успішно записані!");
            document.getElementById("appointmentModal").style.display = "none";
        } else {
            alert("Сталася помилка при записі.");
        }
    }
}