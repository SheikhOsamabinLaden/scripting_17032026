let greets_p = document.getElementById("greets");
const appointmentsList = document.querySelector(".appointments-list");

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







document.addEventListener('DOMContentLoaded', function() {
    // 1. Логіка привітання (залишається вашою)
    let username = null;
    for (let i of document.cookie.split("; ")) {
        let currCookie = i.split("=");
        if (currCookie[0] == "username") {
            username = currCookie[1];
        }
    }
    console.log("Username from cookie:", username);
    greets_p.innerText = username ? `Вітаємо, ${username}` : "Вітаємо!";

    // 2. Логіка завантаження записів (Заглушка для API)
    async function loadAppointments() {

        let url_appointments = `${window.location.href}/api/appointments`;
        appointments_json = await (await fetch(url_appointments)).json;
        console.log(appointments_json)
        const appointments = [
            {
                id: 101, // ID запису для скасування
                doctorName: "Олександр Іванович",
                occupation: "Кардіолог",
                time: "14:30, 25 Травня"
            },
            {
                id: 102,
                doctorName: "Марія Василівна",
                occupation: "Терапевт",
                time: "09:00, 26 Травня"
            }
        ];
        appointmentsList.innerHTML = "";

        if (appointments.length === 0) {
            appointmentsList.innerHTML = "<p>У вас поки немає запланованих прийомів.</p>";
            return;
        }

        appointments_json.forEach(app => {
            // Створюємо HTML картки
            const cardHTML = `
                <div class="appointment-card" data-id="${app.id}">
                    <div class="appointment-info">
                        <h3>${app.doctorName}</h3>
                        <p class="occupation">${app.occupation}</p>
                        <p class="time">Час прийому: ${app.time}</p>
                    </div>
                    <div class="appointment-actions">
                        <button class="btn-cancel" onclick="cancelAppointment(${app.id})">Скасувати запис</button>
                    </div>
                </div>
            `;
            appointmentsList.innerHTML += cardHTML;
        });
    }

    // Викликаємо функцію при завантаженні сторінки
    loadAppointments();
});

// Функція для скасування запису
window.cancelAppointment = async function(appointmentId) {
    const isConfirmed = confirm("Ви впевнені, що хочете скасувати цей запис?");
    
    if (isConfirmed) {
        console.log(`Відправка запиту на скасування запису з ID: ${appointmentId}`);
        
        // TODO: Згодом додати реальний запит до API:
        // await fetch(`/api/cancel-appointment/${appointmentId}`, { method: 'DELETE' });

        // Поки що просто видаляємо картку візуально (через DOM)
        const cardToRemove = document.querySelector(`.appointment-card[data-id="${appointmentId}"]`);
        if (cardToRemove) {
            cardToRemove.remove();
        }

        // Перевіряємо, чи залишились ще картки, якщо ні - показуємо повідомлення
        const remainingCards = document.querySelectorAll(".appointment-card");
        if (remainingCards.length === 0) {
            appointmentsList.innerHTML = "<p>У вас поки немає запланованих прийомів.</p>";
        }
    }
};


