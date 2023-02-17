import json
from flask import Flask, session, request, redirect, url_for, render_template
from setup_db import execute_query
from sqlite3 import IntegrityError
from collections import namedtuple


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', 'POST'])
def home():
    courses = [c_name[0] for c_name in execute_query("SELECT name FROM courses")]
    if 'email' in session:
        str = f'Logged in as {session["email"]}'
        return render_template("index.html", str=str, courses=courses)
    else:
        str = 'You are not logged in'
        return render_template("index.html", str=str, courses=courses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        details = execute_query(
            f"SELECT email,password FROM users WHERE email='{email}' AND password='{password}'")
        d1, d2 = details[0]
        session['email'] = d1
        return redirect(url_for('home'))
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_name = request.form["s_name"].title()
        course_name = request.form["c_name"]
        student_email = request.form["s_email"]
        execute_query(
            f"INSERT INTO students VALUES(NULL,'{student_name}','{student_email}')")
        student_id = [s_id[0] for s_id in execute_query(
            f"SELECT id FROM students WHERE name='{student_name}'")]
        course_id = [c_id[0] for c_id in execute_query(
            f"SELECT id FROM courses WHERE name='{course_name}'")]
        execute_query(
            f"INSERT INTO students_courses VALUES (NULL, '{student_id[0]}', '{course_id[0]}')")
        message = f"{student_name} has been added & associated"
        return render_template("add_student.html", message=message)
    else:
        return render_template("add_student.html")


@app.route('/course_list', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # first section: adding course
        add_course_name = request.form['course']
        teacher = request.form['teacher']
        description = request.form['desc_']
        t_id = [i[0] for i in execute_query(
            f"SELECT id FROM teachers WHERE name='{teacher}'")]
        execute_query(
            f"INSERT INTO courses VALUES(NULL,'{add_course_name}','{description}','{t_id[0]}')")
        message = f"Course {add_course_name} have been added"
        teachers = [t[0] for t in execute_query("SELECT name FROM teachers")]
        return redirect(url_for('search'))
    else:
        teachers = [t[0] for t in execute_query("SELECT name FROM teachers")]
        courses = execute_query("SELECT * FROM courses")
        return render_template("course_list.html", courses=courses, teachers=teachers)


@app.route('/course/<course_id>')
def show_course(course_id):
    c_name = [c_id[0] for c_id in execute_query(
        f"SELECT name FROM courses WHERE id={course_id}")]
    teacher_id = [t_id[0] for t_id in execute_query(
        f"SELECT teacher_id FROM courses WHERE id={course_id}")]
    teacher_name = [t_name[0] for t_name in execute_query(
        f"SELECT name FROM teachers WHERE id={teacher_id[0]}")]
    message = f"Welcome To Course {c_name[0]}".title()
    student_ids = [s_id[0] for s_id in execute_query(
        f"SELECT student_id FROM students_courses WHERE course_id={course_id}")]
    students_names = [[s_name[0] for s_name in execute_query(
        f"SELECT name FROM students WHERE id={student_id}")] for student_id in student_ids]
    return render_template("show_course.html", teacher_name=teacher_name, c_name=c_name, message=message, students_names=students_names)


@app.route('/regsiter/<student_id>/<course_id>')
def register(student_id, course_id):
    try:
        execute_query(
            f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id}', '{course_id}')")
    except IntegrityError:
        return f"{student_id} is already registered to {course_id}"
    return redirect(url_for('registrations', student_id=student_id))


@app.route('/registrations/<student_id>')
def registrations(student_id):
    # 1. Get course IDs for this student using student_courses
    # 2. Get course names using course IDs
    # course_ids=execute_query(f"SELECT course_id FROM students_courses WHERE student_id={student_id}")
    # clean_ids=[ c[0] for c in course_ids]
    # course_names=[]
    # for i in clean_ids:
    #     course_names.append(execute_query(f"SELECT name FROM courses WHERE id={i}"))
    # student_name=execute_query(f"SELECT name FROM students WHERE id={student_id}")
    # return render_template("registrations.html", student_name=student_name, course_names=course_names)
    course_names = execute_query(f"""
        SELECT courses.name, courses.teacher_id FROM courses
        JOIN students_courses on students_courses.course_id=courses.id
        WHERE students_courses.student_id={student_id}
    """)
    courses = []
    # the challenge is to do it in one line !
    for course_tuple in course_names:
        course = namedtuple("Course", ["name", "teacher"])
        course.name = course_tuple[0]
        course.teacher = course_tuple[1]
        courses.append(course)
    # course=namedtupe("Course", ["name","teacher"])
    # course.name="alon"
    # course.teacher="tal"
    return render_template("registrations.html", courses=courses)


# @app.route('/register/<student_id>/<course_id>')
# def register(student_id, course_id):
#     # This endpoint inserts a student into students_courses table so student_id
#     # is registered to course_id. Then show all courses for this student.
#     execute_query(f"INSERT INTO students_courses VALUES (NULL, '{student_id}', '{course_id}')")
#     return redirect(url_for('registrations', student_id=student_id))


# TODO add /registrations endpoint to show all registered students and students
# for testing: translate from course id to course name

@app.route('/course_name/<id>')
def course(id):
    name = execute_query(f"SELECT name FROM courses WHERE id={id}")
    return json.dumps(name)
