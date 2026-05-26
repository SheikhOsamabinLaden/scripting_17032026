let greets_p = document.getElementById("greets");
const appointmentsList = document.querySelector(".appointments-list");

document.addEventListener('DOMContentLoaded', async function() {
    let username = null;
    for (let i of document.cookie.split("; ")) {
        let currCookie = i.split("=");
        if (currCookie[0] == "username") {
            username = currCookie[1];
        }
    }
    greets_p.innerText = username ? `Вітаємо, ${username}` : "Вітаємо!";

    async function loadAppointments() {
        let res = await fetch(`/api/appointments`);
        
        if (res.status === 401) {
            window.location.href = "/login";
            return;
        }

        let appointments_json = await res.json();
        appointmentsList.innerHTML = "";

        if (appointments_json.length === 0) {
            appointmentsList.innerHTML = "<p>У вас поки немає запланованих прийомів.</p>";
            return;
        }

        appointments_json.forEach(app => {
            let dateObj = new Date(app.time);
            let formattedTime = dateObj.toLocaleString("uk-UA", { 
                day: 'numeric', month: 'long', hour: '2-digit', minute:'2-digit'
            });

            const cardHTML = `
                <div class="appointment-card" data-id="${app.id}">
                    <div class="appointment-info">
                        <h3>Лікар: ${app.doctorName}</h3>
                        <p class="occupation">${app.occupation}</p>
                        <p class="time">Час прийому: <b>${formattedTime}</b></p>
                    </div>
                    <div class="appointment-actions">
                        <button class="btn-cancel" onclick="cancelAppointment(${app.id})">Скасувати запис</button>
                    </div>
                </div>
            `;
            appointmentsList.innerHTML += cardHTML;
        });
    }

    loadAppointments();
});

window.cancelAppointment = async function(appointmentId) {
    const isConfirmed = confirm("Ви впевнені, що хочете скасувати цей запис?");
    
    if (isConfirmed) {
        let res = await fetch(`/api/appointments/${appointmentId}`, { 
            method: 'DELETE' 
        });

        if (res.ok) {
            const cardToRemove = document.querySelector(`.appointment-card[data-id="${appointmentId}"]`);
            if (cardToRemove) {
                cardToRemove.remove();
            }

            const remainingCards = document.querySelectorAll(".appointment-card");
            if (remainingCards.length === 0) {
                appointmentsList.innerHTML = "<p>У вас поки немає запланованих прийомів.</p>";
            }
        } else {
            alert("Помилка під час скасування запису.");
        }
    }
};