from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- LOGIN ----------------
@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email=? AND otp=?", (email,password)).fetchone()

    if user:
        session['user'] = email
        return redirect('/dashboard')

    return "Login Failed"

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template("dashboard.html")

# ---------------- PRODUCTS ----------------
@app.route('/products')
def products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()
    return render_template("products.html", products=products)

# ---------------- TRACKING ----------------
@app.route('/tracking/<int:id>')
def tracking(id):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    transactions = conn.execute("SELECT * FROM transactions WHERE product_id=?", (id,)).fetchall()
    return render_template("tracking.html", product=product, transactions=transactions)

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    if session.get('user') not in ["musthafa@purplerock.com","vir@purplerock.com"]:
        return "⚠️ Admin access only"

    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    return render_template("admin.html", users=users)

app.run(host="0.0.0.0", port=5000)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
