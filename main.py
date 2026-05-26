from flask import Flask, jsonify, request, redirect, url_for, session, render_template_string, render_template, make_response
from doctors import *
from users import *
import db
from functools import wraps
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
            user_data = db.get_user_by_login(login)[0]
            session["id"] = user_data["id"]
            session["login"] = login
            session["password"] = password
            session["is_admin"] = user_data.get("is_admin", False) 
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

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            return "Доступ заборонено (Тільки для адміністраторів)", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin")
@admin_required
def admin_dashboard():
    return render_template("admin.html")

@app.route("/admin/users", methods=["GET", "POST"])
@admin_required
def admin_users():
    if request.method == "POST":
        db.create_user(
            request.form.get("login"),
            request.form.get("password"),
            request.form.get("is_admin") == "on"
        )
        return redirect(url_for("admin_users"))
    return render_template("admin_users.html", users=db.get_users())

@app.route("/admin/users/delete/<int:id>")
@admin_required
def admin_delete_user(id):
    db.delete_user(id)
    return redirect(url_for("admin_users"))

@app.route("/admin/users/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_edit_user(id):
    if request.method == "POST":
        db.update_user(
            id, 
            request.form.get("login"), 
            request.form.get("password"), 
            request.form.get("is_admin") == "on"
        )
        return redirect(url_for("admin_users"))
    user = db.get_user_by_id(id)[0]
    return render_template("admin_users_edit.html", user=user)

@app.route("/admin/occupations", methods=["GET", "POST"])
@admin_required
def admin_occupations():
    if request.method == "POST":
        db.create_occupation(request.form.get("name"))
        return redirect(url_for("admin_occupations"))
    return render_template("admin_occupations.html", occupations=db.get_occupations())

@app.route("/admin/occupations/delete/<int:id>")
@admin_required
def admin_delete_occupation(id):
    db.delete_occupation(id)
    return redirect(url_for("admin_occupations"))

@app.route("/admin/occupations/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_edit_occupation(id):
    if request.method == "POST":
        db.update_occupation(id, request.form.get("name"))
        return redirect(url_for("admin_occupations"))
    occupation = db.get_occupation_by_id(id)[0]
    return render_template("admin_occupations_edit.html", occupation=occupation)

@app.route("/admin/doctors", methods=["GET", "POST"])
@admin_required
def admin_doctors():
    if request.method == "POST":
        db.create_doctor(
            request.form.get("name"),
            request.form.get("patronym"),
            request.form.get("occupation_id")
        )
        return redirect(url_for("admin_doctors"))
    return render_template("admin_doctors.html", doctors=db.get_doctors(), occupations=db.get_occupations())

@app.route("/admin/doctors/delete/<int:id>")
@admin_required
def admin_delete_doctor(id):
    db.delete_doctor(id)
    return redirect(url_for("admin_doctors"))

@app.route("/admin/doctors/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_edit_doctor(id):
    if request.method == "POST":
        db.update_doctor(
            id,
            request.form.get("name"),
            request.form.get("patronym"),
            request.form.get("occupation_id")
        )
        return redirect(url_for("admin_doctors"))
    doctor = db.get_doctor_by_id(id)[0]
    return render_template("admin_doctors_edit.html", doctor=doctor, occupations=db.get_occupations())

@app.route("/admin/appointments", methods=["GET", "POST"])
@admin_required
def admin_appointments():
    if request.method == "POST":
        db.create_appointment(
            request.form.get("appointed_at"),
            request.form.get("doctor_id"),
            request.form.get("user_id"),
            request.form.get("comments")
        )
        return redirect(url_for("admin_appointments"))
    return render_template("admin_appointments.html", appointments=db.get_appointments(), doctors=db.get_doctors(), users=db.get_users())

@app.route("/admin/appointments/delete/<int:id>")
@admin_required
def admin_delete_appointment(id):
    db.delete_appointment(id)
    return redirect(url_for("admin_appointments"))

@app.route("/admin/appointments/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_edit_appointment(id):
    if request.method == "POST":
        db.update_appointment(
            id,
            request.form.get("appointed_at"),
            request.form.get("doctor_id"),
            request.form.get("user_id"),
            request.form.get("comments")
        )
        return redirect(url_for("admin_appointments"))
    appointment = db.get_appointment_by_id(id)[0]
    return render_template("admin_appointments_edit.html", appointment=appointment, doctors=db.get_doctors(), users=db.get_users())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)