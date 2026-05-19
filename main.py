from flask import Flask, jsonify, request, redirect, url_for, session, render_template_string, render_template, make_response
from doctors import *
from users import *
import db
app = Flask(__name__)
app.secret_key = "pcmtofolwnzucvotykymgicopew,sjvlgm,6fp8fo6emn1wsn35v2j4"

@app.route("/api/doctors", methods=["GET"])
def api_doctors():
    doctors = db.get_doctors()
    return jsonify(doctors)

def get_doctor_info(doctors, doctor_id):
    for doctor in doctors:
        if doctor['id'] == doctor_id:
            return doctor['name'], doctor.get('occupations', {}).get('name', 'Невідомо')
    return "Невідомо", "Невідомо"

@app.route("/api/appointments", methods=["GET", "POST"])
def api_appointments():
    if request.method == "GET":
        if "id" not in session:
            return jsonify({"error": "Unauthorized"}), 401
            
        appointments = db.get_appointments()
        users_appointments = []
        doctors = db.get_doctors_with_occupation_names()
        
        for i in appointments:
            if i["user_id"] == session["id"]:
                doc_name, doc_occ = get_doctor_info(doctors, i["doctor_id"])
                users_appointments.append({
                    "id": i["id"],
                    "doctorName": doc_name,
                    "occupation": doc_occ,
                    "time": i["appointed_at"]
                })
        return jsonify(users_appointments)
        
    elif request.method == "POST":
        if "id" not in session:
            return jsonify({"error": "Unauthorized"}), 401
            
        data = request.get_json()
        appointed_at = data.get("time")
        doctor_id = data.get("doctor_id")
        
        db.create_appointment(appointed_at, doctor_id, session["id"])
        return jsonify({"status": "success"})

@app.route("/api/appointments/<int:app_id>", methods=["DELETE"])
def api_delete_appointment(app_id):
    if "id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    db.delete_appointment(app_id)
    return jsonify({"status": "success"})

@app.route("/api/appointments/doctor/<int:doctor_id>", methods=["GET"])
def api_doctor_appointments(doctor_id):
    appointments = db.get_appointments()
    # Повертаємо список зайнятих годин для конкретного лікаря
    booked_times = [app["appointed_at"] for app in appointments if app["doctor_id"] == doctor_id]
    return jsonify(booked_times)

@app.route("/api/occupations", methods=["GET"])
def api_occupations():
    return jsonify(db.get_occupations()) 

@app.route("/api/contact", methods=["POST"])
def api_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(f"name: {name}\nemail: {email}\n------------\nmessage: {message}")
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("index.html", session=session)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('pass')
        login_try = db.check_user(login, password)
        if login_try:
            session["id"] = db.get_user_by_login(login)[0]["id"]
            session["login"] = login
            session["password"] = password
            res = make_response(redirect(url_for("index")))
            res.set_cookie("username", login)
            return res
        else:
           return render_template("login.html", incorrect=True, login_value=login)

    elif request.method == "GET":
        return render_template("login.html")

@app.route("/profile")
def profile():
    if session.get("login") is None:
        return redirect(url_for("login"))
    return render_template("profile.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)