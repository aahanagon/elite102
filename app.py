# app.py
from sqlite3 import IntegrityError
import os
import sqlite3
from flask import (
    Flask, render_template, request, redirect, session, url_for, flash
)
from src.database import initialize_db, DB_NAME
from src.crud import create_user, deposit, withdraw, check_balance, get_transactions

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ensure DB exists
initialize_db()


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pw = request.form["password"]
        db = get_db()
        user = db.execute(
            "SELECT id,name FROM users WHERE email=? AND password=?",
            (email, pw)
        ).fetchone()
        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
+        name  = request.form["name"]
+        email = request.form["email"]
+        pw    = request.form["password"]
+        try:
+            create_user(name, email, pw)
+            flash("✅ Registered! Please log in.", "success")
+            return redirect(url_for("login"))
+        except IntegrityError:
+            # this happens if email already exists
+            flash("❌ That email is already registered. Try logging in or use a different email.", "danger")
     return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    uid = session.get("user_id")
    if not uid:
        return redirect(url_for("login"))
    bal = check_balance(uid)
    return render_template("dashboard.html", name=session["user_name"], balance=bal)


@app.route("/deposit", methods=["POST"])
def do_deposit():
    amt = float(request.form["amount"])
    deposit(session["user_id"], amt)
    flash(f"Deposited ${amt:.2f}", "success")
    return redirect(url_for("dashboard"))


@app.route("/withdraw", methods=["POST"])
def do_withdraw():
    amt = float(request.form["amount"])
    try:
        withdraw(session["user_id"], amt)
        flash(f"Withdrew ${amt:.2f}", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("dashboard"))


@app.route("/transactions")
def transactions():
    uid = session.get("user_id")
    if not uid:
        return redirect(url_for("login"))
    txs = get_transactions(uid)
    return render_template("transactions.html", transactions=txs)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
