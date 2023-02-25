import json
from flask import Flask, session, request, redirect, url_for, render_template, abort
from setup_db import execute_query
from sqlite3 import IntegrityError
# from collections import namedtuple

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.before_request
def auth():
    if "role" not in session.keys():
        session["role"] = "Guest"
        session["email"] = "guest@gmail.com"
    if session["role"] != 'admin':
        if "courses" in request.full_path:
            return abort(403)
        if "students" in request.full_path:
            return abort(403)
    if session["role"] == 'Guest':
        if "profile" in request.full_path:
            return abort(403)


@app.route('/', methods=['GET', 'POST'])
def home():
    courses = [(c_name[0], c_name[1]) for c_name in execute_query("SELECT id,name FROM courses")]
    str, link, log = navbar_auth()
    return render_template("home.html", courses=courses, str=str, link=link, log=log)


def navbar_auth():
    if session["role"] != 'Guest':
        if session["role"] == 'admin':
            str = f'Logged in as: {session["role"]}'
            log = "Logout"
            link = "/logout"
        elif session["role"] == 'student':
            str = f'Logged in as: {session["email"]}'
            log = "Logout"
            link = "/logout"
    else:
        str = f'Welcome {session["role"]}'
        log = "Login"
        link = "/login"
    return str, link, log


def authenticate(email, password):
    role = execute_query(f"SELECT role FROM users WHERE email='{email}' AND password='{password}'")
    if role == []:
        return None
    else:
        return role[0][0]


@app.route('/results', methods=['GET', 'POST'])
def results():
    str, link, log = navbar_auth()
    searchbox = request.args['searchbox']
    result = f"This is what I have found for '{searchbox}'"
    div = """<div class="message">"""
    div_ = "</div>"
    if searchbox == '':
        return render_template("results.html", result=result, div=div, div_=div_)
    else:
        courses = execute_query(f"SELECT * FROM courses WHERE name LIKE '%{searchbox}%'")
        students = execute_query(f"SELECT * FROM students WHERE name LIKE '%{searchbox}%'")
        return render_template("results.html", courses=courses, students=students, result=result, div=div, div_=div_, link=link, log=log)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = authenticate(request.form["email"], request.form["password"])
        if role is None:
            return abort(403)
        else:
            session["role"] = role
            session["email"] = request.form["email"]
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('role', None)
    return redirect(url_for('home'))


@app.route('/students', methods=['GET', 'POST'])
def students():
    str, link, log = navbar_auth()
    students = execute_query("SELECT * FROM students")
    if request.method == 'POST':
        # FORM1 : ADD STUDENT
        if "form-submit" in request.form:
            student_name = request.form["s_name"].title()
            student_email = request.form["s_email"]
            execute_query(f"INSERT INTO students VALUES(NULL,'{student_name}','{student_email}')")
        # FORM2 : ASSOCIATE STUDENT
        elif "form2-submit" in request.form:
            student_name = request.form["s_name"].title()
            student_email = request.form["s_email"]
            course_name = request.form["c_name"]
            student_id = [s_id[0] for s_id in execute_query(
                f"SELECT id FROM students WHERE name='{student_name}'")]
            course_id = [c_id[0] for c_id in execute_query(
                f"SELECT id FROM courses WHERE name='{course_name}'")]
            execute_query(
                f"INSERT INTO students_courses VALUES (NULL, '{student_id[0]}', '{course_id[0]}')")
        return redirect(url_for('students'))
    return render_template("students.html", students=students, link=link, log=log)


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    str, link, log = navbar_auth()
    if request.method == 'POST':
        # first section: adding course
        add_course_name = request.form['course']
        teacher = request.form['teacher']
        description = request.form['desc_']
        t_id = [i[0] for i in execute_query(
            f"SELECT id FROM teachers WHERE name='{teacher}'")]
        execute_query(
            f"INSERT INTO courses VALUES(NULL,'{add_course_name}','{description}','{t_id[0]}')")
        teachers = [t[0] for t in execute_query("SELECT name FROM teachers")]
        return redirect(url_for('courses'))
    else:
        teachers = [t[0] for t in execute_query("SELECT name FROM teachers")]
        courses = execute_query("SELECT * FROM courses")
        return render_template("courses.html", courses=courses, teachers=teachers, link=link, log=log)


@app.route('/course/<course_id>')
def show_course(course_id):
    str, link, log = navbar_auth()
    c_name = [c_id[0] for c_id in execute_query(
        f"SELECT name FROM courses WHERE id={course_id}")]
    teacher_id = [t_id[0] for t_id in execute_query(
        f"SELECT teacher_id FROM courses WHERE id={course_id}")]
    teacher_details = [(teacher[0], teacher[1]) for teacher in execute_query(
        f"SELECT name,email FROM teachers WHERE id={teacher_id[0]}")]
    message = f"Welcome To Course {c_name[0]}".title()
    student_ids = [s_id[0] for s_id in execute_query(
        f"SELECT student_id FROM students_courses WHERE course_id={course_id}")]
    students = [[(student[0], student[1]) for student in execute_query(
        f"SELECT id, name FROM students WHERE id={student_id}")] for student_id in student_ids]
    return render_template("course.html", teacher_details=teacher_details, c_name=c_name, message=message, students=students, link=link, log=log)


@app.route('/profile/<int:student_id>')
def profile(student_id):
    str, link, log = navbar_auth()
    course_ids = execute_query(f"SELECT course_id FROM students_courses WHERE student_id={student_id}")
    clean_ids = [c[0] for c in course_ids]
    course_names = []
    for i in clean_ids:
        course_names.append(execute_query(f"SELECT name FROM courses WHERE id={i}"))
    student_details = execute_query(f"SELECT * FROM students WHERE id={student_id}")
    return render_template("profile.html", student_details=student_details, course_names=course_names, link=link, log=log, student_id=student_id)


@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update(student_id):
    str, link, log = navbar_auth()
    if request.method == 'POST':
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        if (email != '') or (phone != '') or (password != ''):
            execute_query(f"UPDATE students SET email='{email}',phone='{phone}' WHERE id={student_id}")
            db_email = execute_query(f"SELECT email FROM students WHERE id={student_id}")
            execute_query(f"UPDATE users SET password='{password}' WHERE email='{db_email[0][0]}'")
        return redirect(url_for("profile", student_id=student_id))
    else:
        return render_template("update.html", link=link, log=log, student_id=student_id)


@app.route('/register/<student_id>/<course_id>')
def register(student_id, course_id):
    try:
        execute_query(
            f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id}', '{course_id}')")
    except IntegrityError:
        return f"{student_id} is already registered to {course_id}"
    return redirect(url_for('registrations', student_id=student_id))


@app.route('/course_name/<id>')
def course(id):
    name = execute_query(f"SELECT name FROM courses WHERE id={id}")
    return json.dumps(name)
