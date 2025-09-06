import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "clarizen_secret"

DB = "portfolio.db"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --- DB Setup ---
def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    image TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    message TEXT)''')
    con.commit()
    con.close()

init_db()

# --- Public Routes ---
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/projects')
def projects():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cur.fetchall()
    con.close()
    return render_template("projects.html", projects=projects)

@app.route('/about')
def about():
    return render_template("about.html")



@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, msg))
        con.commit()
        con.close()
        return redirect(url_for('contact'))
    return render_template("contact.html")

# --- Auth ---
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form['username'] == "admin" and request.form['password'] == "1234":
            session['admin'] = True
            return redirect(url_for('admin'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

# --- Admin Panel ---
@app.route('/admin', methods=["GET", "POST"])
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))

    con = sqlite3.connect(DB)
    cur = con.cursor()

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['description']
        file = request.files['image']

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            img_path = f"/static/uploads/{filename}"
        else:
            img_path = ""

        cur.execute("INSERT INTO projects (title, description, image) VALUES (?, ?, ?)", (title, desc, img_path))
        con.commit()

    cur.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cur.fetchall()
    cur.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    con.close()

    return render_template("admin.html", projects=projects, messages=messages)

@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("DELETE FROM projects WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
