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
        phone TEXT,
        blood_group TEXT,
        height REAL,
        weight REAL,
        allergies TEXT,
        emergency_name TEXT,
        emergency_phone TEXT
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

    # ✅ new health fields
    blood_group = request.form.get('blood_group')
    height = request.form.get('height')
    weight = request.form.get('weight')
    allergies = request.form.get('allergies')
    emergency_name = request.form.get('emergency_name')
    emergency_phone = request.form.get('emergency_phone')

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO persons 
        (name, age, email, phone, blood_group, height, weight, allergies, emergency_name, emergency_phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, age, email, phone, blood_group, height, weight, allergies, emergency_name, emergency_phone))
    conn.commit()
    conn.close()
    return redirect('/view')
# --- View all records (used for both /view and /view-all) ---
@app.route('/view')
@app.route('/view-all')
def view_all():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM persons ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return render_template("view.html", rows=rows)
@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM persons WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/view')
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    if request.method == 'POST':
        # collect updated data
        name = request.form.get('name')
        age = request.form.get('age') or None
        email = request.form.get('email')
        phone = request.form.get('phone')
        blood_group = request.form.get('blood_group')
        height = request.form.get('height')
        weight = request.form.get('weight')
        allergies = request.form.get('allergies')
        emergency_name = request.form.get('emergency_name')
        emergency_phone = request.form.get('emergency_phone')

        # update database
        cur.execute("""
            UPDATE persons
            SET name=?, age=?, email=?, phone=?, blood_group=?, height=?, weight=?, allergies=?, emergency_name=?, emergency_phone=?
            WHERE id=?
        """, (name, age, email, phone, blood_group, height, weight, allergies, emergency_name, emergency_phone, id))
        
        conn.commit()
        conn.close()
        return redirect('/view')
    
    # GET method → show form with current values
    cur.execute("SELECT * FROM persons WHERE id=?", (id,))
    person = cur.fetchone()
    conn.close()
    return render_template('edit.html', person=person)

if __name__ == '__main__':
    app.run(debug=True)