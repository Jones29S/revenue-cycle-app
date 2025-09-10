from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_financial_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS revenue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payer TEXT,
        claims INTEGER,
        payments REAL,
        denials INTEGER,
        outstanding REAL
    )''')
    conn.commit()
    conn.close()

init_financial_db()

@app.route("/")
def dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT payer, claims, payments, denials, outstanding FROM revenue")
    data = c.fetchall()
    conn.close()
    return render_template("dashboard.html", data=data)

@app.route("/seed")
def seed_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sample = [
        ("Medicare", 120, 45000.00, 10, 5000.00),
        ("Blue Cross", 95, 38000.00, 5, 3000.00),
        ("Aetna", 80, 32000.00, 8, 4000.00)
    ]
    c.executemany("INSERT INTO revenue (payer, claims, payments, denials, outstanding) VALUES (?, ?, ?, ?, ?)", sample)
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        payer = request.form["payer"]
        claims = int(request.form["claims"])
        payments = float(request.form["payments"])
        denials = int(request.form["denials"])
        outstanding = float(request.form["outstanding"])

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO revenue (payer, claims, payments, denials, outstanding) VALUES (?, ?, ?, ?, ?)",
                  (payer, claims, payments, denials, outstanding))
        conn.commit()
        conn.close()
        return redirect("/")
    
    return render_template("test_add.html")

if __name__ == "__main__":
    app.run(debug=True)
