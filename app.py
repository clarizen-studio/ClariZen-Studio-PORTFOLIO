import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "clarizen_secret"

DB = "portfolio.db"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# --- Database Setup ---
def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # Projects table
    cur.execute('''CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    image TEXT)''')

    # Samples table
    cur.execute('''CREATE TABLE IF NOT EXISTS samples (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    image TEXT)''')

    # Messages table
    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    message TEXT)''')

    # Admin credentials table
    cur.execute('''CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT)''')

    # Default admin user
    cur.execute("SELECT * FROM admin")
    if not cur.fetchone():
        cur.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "1234"))

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


@app.route('/samples')
def samples():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM samples ORDER BY id DESC")
    samples = cur.fetchall()
    con.close()
    return render_template("samples.html", samples=samples)


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
        # FIX: redirect to new page instead of rendering to avoid resubmit issue
        return redirect(url_for('thankyou'))
    return render_template("contact.html")


@app.route('/thankyou')
def thankyou():
    return render_template("thankyou.html")


# --- Auth ---
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        con.close()
        if user:
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))


# --- Admin Dashboard ---
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    return render_template("admin.html")


# --- Projects Management ---
@app.route('/admin/projects', methods=["GET", "POST"])
def admin_projects():
    if not session.get('admin'):
        return redirect(url_for('login'))

    con = sqlite3.connect(DB)
    cur = con.cursor()

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['description']
        file = request.files['image']
        img_path = ""
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            img_path = f"/static/uploads/{filename}"
        cur.execute("INSERT INTO projects (title, description, image) VALUES (?, ?, ?)", (title, desc, img_path))
        con.commit()
        return redirect(url_for('admin_projects'))  # redirect fix

    cur.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cur.fetchall()
    con.close()

    return render_template("admin_projects.html", projects=projects)


@app.route('/delete_project/<int:id>')
def delete_project(id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("DELETE FROM projects WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect(url_for('admin_projects'))


@app.route('/edit_project/<int:id>', methods=["GET", "POST"])
def edit_project(id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    con = sqlite3.connect(DB)
    cur = con.cursor()

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['description']
        file = request.files['image']
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            img_path = f"/static/uploads/{filename}"
            cur.execute("UPDATE projects SET title=?, description=?, image=? WHERE id=?", (title, desc, img_path, id))
        else:
            cur.execute("UPDATE projects SET title=?, description=? WHERE id=?", (title, desc, id))
        con.commit()
        con.close()
        return redirect(url_for('admin_projects'))

    cur.execute("SELECT * FROM projects WHERE id=?", (id,))
    project = cur.fetchone()
    con.close()
    return render_template("edit_project.html", project=project)


# --- Samples Management ---
@app.route('/admin/samples', methods=["GET", "POST"])
def admin_samples():
    if not session.get('admin'):
        return redirect(url_for('login'))

    con = sqlite3.connect(DB)
    cur = con.cursor()

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['description']
        file = request.files['image']
        img_path = ""
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            img_path = f"/static/uploads/{filename}"
        cur.execute("INSERT INTO samples (title, description, image) VALUES (?, ?, ?)", (title, desc, img_path))
        con.commit()
        return redirect(url_for('admin_samples'))  # redirect fix

    cur.execute("SELECT * FROM samples ORDER BY id DESC")
    samples = cur.fetchall()
    con.close()

    return render_template("admin_samples.html", samples=samples)


@app.route('/delete_sample/<int:id>')
def delete_sample(id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("DELETE FROM samples WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect(url_for('admin_samples'))


@app.route('/edit_sample/<int:id>', methods=["GET", "POST"])
def edit_sample(id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    con = sqlite3.connect(DB)
    cur = con.cursor()

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['description']
        file = request.files['image']
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            img_path = f"/static/uploads/{filename}"
            cur.execute("UPDATE samples SET title=?, description=?, image=? WHERE id=?", (title, desc, img_path, id))
        else:
            cur.execute("UPDATE samples SET title=?, description=? WHERE id=?", (title, desc, id))
        con.commit()
        con.close()
        return redirect(url_for('admin_samples'))

    cur.execute("SELECT * FROM samples WHERE id=?", (id,))
    sample = cur.fetchone()
    con.close()
    return render_template("edit_sample.html", sample=sample)


# --- Messages Management ---
@app.route('/admin/messages')
def admin_messages():
    if not session.get('admin'):
        return redirect(url_for('login'))
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    con.close()
    return render_template("admin_messages.html", messages=messages)


# --- Change Credentials ---
@app.route('/admin/credentials', methods=["GET", "POST"])
def admin_credentials():
    if not session.get('admin'):
        return redirect(url_for('login'))

    if request.method == "POST":
        new_user = request.form['username']
        new_pass = request.form['password']
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("UPDATE admin SET username=?, password=? WHERE id=1", (new_user, new_pass))
        con.commit()
        con.close()
        return redirect(url_for('admin'))

    return render_template("admin_credentials.html")


if __name__ == '__main__':
    app.run(debug=True)
