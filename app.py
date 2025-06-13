from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from main import create_connection, create_table  # Fichier qui gère les tâches

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "votre_clé_secrète"

USER_DB = "users.db"

def init_user_db():
    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def connection():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        action = request.form["action"]

        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()

        if action == "register":
            try:
                hashed_password = generate_password_hash(password)
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                # récupérer l'utilisateur pour créer la session
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user = cursor.fetchone()
                session["user_id"] = user[0]
                return redirect(url_for("todo_manager"))
            except sqlite3.IntegrityError:
                return "Nom d'utilisateur déjà pris !"

        elif action == "login":
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user[2], password):
                session["user_id"] = user[0]
                return redirect(url_for("todo_manager"))
            else:
                return "Identifiants incorrects !"
        conn.close()

    return render_template("connection.html")

@app.route("/todo_manager")
def todo_manager():
    if "user_id" not in session:
        return redirect(url_for("connection"))
    return render_template("connexion.html")  # Tu peux connecter ici à la logique de gestion de tâches

if __name__ == "__main__":
    init_user_db()
    app.run(debug=True)
