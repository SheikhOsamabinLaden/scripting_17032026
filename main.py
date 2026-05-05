from flask import Flask, jsonify, request, redirect, url_for, session, render_template_string, render_template, make_response
from doctors import *
from users import *
import db
app = Flask(__name__)
app.secret_key = "pcmtofolwnzucvotykymgicopew,sjvlgm,6fp8fo6emn1wsn35v2j4"
# https://meet.google.com/nbv-ktvd-igi


@app.route("/api/doctors", methods=["GET"])
def api_doctors():
    doctors = db.get_doctors()
    # print(doctors)
    # for i in range(len(doctors)):
    #     doctors[i]["name"] = f"{doctors[i]["name"]} {doctors[i]["patronym"]}"
    return jsonify(db.get_doctors()) #return jsonify(doctors)

def get_doctor_info(doctors, doctor_id):
    for doctor in doctors:
        if doctor['id'] == doctor_id:
            return doctor['name'], doctor['occupations']['name']
    return None, None

@app.route("/api/appointments", methods=["GET"])
def api_appointments():
    appointments = db.get_appointments()
    users_appointments = []
    print(appointments)
    doctors = db.get_doctors_with_occupation_names()
    for i in appointments:
        if (i["user_id"] == session["id"]):
            users_appointments.append({
                "doctorName": get_doctor_info(doctors, i["doctor_id"])["name"],
                "occupation": get_doctor_info(doctors, i["doctor_id"])["occupation"],
                "time": i["appointed_at"]
            })
    return jsonify(users_appointments)

@app.route("/api/occupations", methods=["GET"])
def api_occupations():
    return jsonify(db.get_occupations()) #return jsonify(occupations)

@app.route("/api/contact", methods=["POST"])
def api_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(f"""
name: {name}
email: {email}
------------
message: {message}""")
    return redirect(url_for("index"))

@app.route("/")
def index():
    test = "12345678"
    return render_template("index.html", test=test, session=session)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('pass')
        print (f"{login} {password}")
        # for i in users:
        #     if i["login"] == login and i["password"] == password:
        #         session["login"] = login
        #         session["password"] = password
        #         res = make_response(redirect(url_for("index")))
        #         res.set_cookie("username", i["login"])
        #         return res
        # else:
        #     return "incorrect password"
        login_try = db.check_user(login, password)
        if  login_try:
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
    if (session.get("login") is None):
        return redirect(url_for("login"))
    return render_template("profile.html")

@app.route("/search")
def search():
    # if (session.get("login") is None):
    #     return redirect(url_for("login"))
    return render_template("search.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)