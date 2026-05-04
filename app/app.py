from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB = "database.db"

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

        return redirect("/")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    names = cursor.fetchall()
    conn.close()

    return render_template("index.html", names=names)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
