from flask import Flask, jsonify, request, redirect, url_for, session, render_template_string, render_template

app = Flask(__name__)
app.secret_key = "pcmtofolwnzucvotykymgicopew,sjvlgm,6fp8fo6emn1wsn35v2j4"

doctors = [
    {"name": "Валентина Петрівна",
    "occupation": "проктологія",
    "excerience": "17 років"},

    {"name": "Петро Іванович",
    "occupation": "кардіологія",
    "excerience": "23 роки"},
]

@app.route("/api/doctors", methods=["GET"])
def api_doctors():
    return jsonify(doctors)

@app.route("/")
def index():
    test = "12345678"
    return render_template("index.html", test=test)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('pass')
        print (f"{login} {password}")
        if login == "a" and password == "b":
            redirect(url_for("index"))
        else:
            return "b"
    elif request.method == "GET":
        return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)