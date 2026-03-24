from flask import Flask, jsonify, request, redirect, url_for, session, render_template_string, render_template, make_response
from doctors import *
from users import *
app = Flask(__name__)
app.secret_key = "pcmtofolwnzucvotykymgicopew,sjvlgm,6fp8fo6emn1wsn35v2j4"




@app.route("/api/doctors", methods=["GET"])
def api_doctors():
    return jsonify(doctors)

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
        for i in users:
            if i["login"] == login and i["password"] == password:
                session["login"] = login
                session["password"] = password
                res = make_response(redirect(url_for("index")))
                res.set_cookie("username", i["login"])
                return res
        else:
            return "incorrect password"
    elif request.method == "GET":
        return render_template("login.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)