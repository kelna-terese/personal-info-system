from flask import Flask, render_template, request, redirect
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "PIS.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT,
        phone TEXT
    )
    """)
    conn.commit()
    conn.close()

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    age = request.form.get('age') or None
    email = request.form.get('email')
    phone = request.form.get('phone')
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO persons (name, age, email, phone) VALUES (?, ?, ?, ?)",
                (name, age, email, phone))
    conn.commit()
    conn.close()
    return redirect('/view')

@app.route('/view')
def view():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, age, email, phone FROM persons")
    rows = cur.fetchall()
    conn.close()
    return render_template('view.html', persons=rows)
@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM persons WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/view')
if __name__ == '__main__':
    app.run(debug=True)