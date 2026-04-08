from flask import Flask, render_template, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# CREATE DB IF NOT EXISTS
if not os.path.exists("database.db"):
    conn = sqlite3.connect("database.db")
    conn.execute("CREATE TABLE users (email TEXT, password TEXT)")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()

    if user:
        session['user'] = email
        return redirect('/dashboard')

    return "Login Failed"

# REMOVE extra app.run() ❌

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
