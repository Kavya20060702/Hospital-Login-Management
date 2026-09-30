from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# Demo users
users = {
    "admin": {
        "password": "admin123",
        "role": "Administrator"
    },
    "doctor": {
        "password": "doctor123",
        "role": "Doctor"
    },
    "nurse": {
        "password": "nurse123",
        "role": "Nurse"
    }
}


@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["username"] = username
            session["role"] = users[username]["role"]

            return redirect(url_for("dashboard"))

        error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hospital Dashboard</title>
        <link rel="stylesheet"
              href="{url_for('static', filename='style.css')}">
    </head>

    <body>

        <div class="dashboard">

            <div class="topbar">
                <h1>🏥 Hospital Management System</h1>

                <a href="/logout" class="logout">
                    Logout
                </a>
            </div>

            <div class="welcome">
                <h2>Welcome, {session["username"].title()}!</h2>
                <p>Role: {session["role"]}</p>
            </div>

            <div class="cards">

                <div class="card">
                    <h3>👨‍⚕️ Doctors</h3>
                    <p>Manage doctors and their schedules.</p>
                </div>

                <div class="card">
                    <h3>🧑‍🤝‍🧑 Patients</h3>
                    <p>View and manage patient records.</p>
                </div>

                <div class="card">
                    <h3>📅 Appointments</h3>
                    <p>Manage hospital appointments.</p>
                </div>

                <div class="card">
                    <h3>💊 Pharmacy</h3>
                    <p>Manage medicines and prescriptions.</p>
                </div>

            </div>

        </div>

    </body>
    </html>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)