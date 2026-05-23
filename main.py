from flask import Flask, render_template, request, session, redirect,url_for
import sqlite3
import hashlib
import re
app = Flask(__name__)
app.secret_key = "cybersecretkey" 

@app.route("/users")
def users():

    conn = sqlite3.connect("password_history.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    data = cursor.fetchall()

    conn.close()

    return str(data)

common_passwords = [
    "123456",
    "password",
    "admin",
    "qwerty",
    "password123"
]

@app.route("/", methods=["GET", "POST"])
def login_page():

    result = ""
    strength = ""

    if request.method == "POST":

        password = request.form["password"]

        score = 0

        if len(password) >= 8:
            score += 1

        if re.search(r"[A-Z]", password):
            score += 1

        if re.search(r"[a-z]", password):
            score += 1

        if re.search(r"[0-9]", password):
            score += 1

        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 1

        if score <= 2:
            strength = "Weak"

        elif score <= 4:
            strength = "Medium"

        else:
            strength = "Strong"

        result = f"Password Strength: {strength}"

        if password.lower() in common_passwords:
            result += " | Weak Password Vulnerability Detected!"

        # Database
        conn = sqlite3.connect("password_history.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash TEXT
        )
        """)

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        cursor.execute(
            "SELECT * FROM passwords WHERE password_hash = ?",
            (hashed_password,)
        )

        existing = cursor.fetchone()

        if existing:
            result += " | Password already used!"

        else:
            cursor.execute(
                "INSERT INTO passwords (password_hash) VALUES (?)",
                (hashed_password,)
            )

            conn.commit()

            result += " | Password stored securely!"

        conn.close()

    return render_template(
        "index.html",
        result=result
    )
# ======================================
# CREATE USERS TABLE
# ======================================

conn = sqlite3.connect("password_history.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    email TEXT,

    password TEXT
)
""")

conn.commit()
conn.close()

# ======================================
# SIGNUP PAGE
# ======================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # HASH PASSWORD
        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        # DATABASE CONNECTION
        conn = sqlite3.connect("password_history.db")
        cursor = conn.cursor()

        # INSERT USER
        cursor.execute(

            "INSERT INTO users(username, email, password) VALUES (?, ?, ?)",

            (username, email, hashed_password)

        )

        conn.commit()
        conn.close()

        return redirect(url_for("login_page"))

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)