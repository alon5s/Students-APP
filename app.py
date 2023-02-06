from flask import Flask,session,request,redirect,url_for,render_template
app = Flask(__name__)
from setup_db import execute_query

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET','POST'])
def home():
    if 'email' in session:
        str = f'Logged in as {session["email"]}'
        return render_template("index.html", str=str)
    else:
        str = 'You are not logged in'
        return render_template("index.html", str=str)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    if request.method=='POST':
        email = request.form["email"]
        password = request.form["password"]
        details = execute_query(f"SELECT email,password FROM users WHERE email='{email}' AND password='{password}'")
        d1,d2 = details[0]
        session['email'] = d1
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route('/addstudent', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template("add_student.html")
    if request.method == 'POST':
        name = request.form["name"].title()
        email = request.form["email"]
        execute_query(f"INSERT INTO students VALUES(NULL,'{name}','{email}')")
        message = f"{name} have been added"
        return render_template("add_student.html", message=message)
        

@app.route('/course/add', methods=['GET','POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course'].capitalize()
        teacher = request.form['teacher']
        description =  request.form['desc_']
        t_id = [ i[0] for i in execute_query(f"SELECT id FROM teachers WHERE name='{teacher}'") ]
        execute_query(f"INSERT INTO courses VALUES(NULL,'{course_name}','{description}','{t_id[0]}')")
        message = "Course have been added"
        teachers = [ t[0] for t in execute_query("SELECT name FROM teachers") ]
        return render_template("add_course.html", message=message, teachers=teachers)
    else:
        teachers = [ t[0] for t in execute_query("SELECT name FROM teachers") ]
        return render_template("add_course.html", teachers=teachers)

@app.route('/course_list', methods=['GET','POST'])
def search():
    if request.method == 'GET':
        courses = execute_query("SELECT * FROM courses")
        return render_template("course_list.html", courses=courses)
    if request.method == 'POST':
        student_name = request.form["s_name"].title()
        course_name = request.form["c_name"].title()
        student_id = [ s_id[0] for s_id in execute_query(f"SELECT id FROM students WHERE name='{student_name}'")]
        course_id = [ c_id[0] for c_id in execute_query(f"SELECT id FROM courses WHERE name='{course_name}'")]
        execute_query(f"INSERT INTO students_courses VALUES (NULL, '{student_id[0]}', '{course_id[0]}')")
        return redirect(url_for('search'))


@app.route('/course/<course_id>')
def show_course(course_id):
    c_name = [ c_id[0] for c_id in execute_query(f"SELECT name FROM courses WHERE id={course_id}") ]
    teacher_id = [ t_id[0] for t_id in execute_query(f"SELECT teacher_id FROM courses WHERE id={course_id[0]}") ]
    teacher_name = [ t_name[0] for t_name in execute_query(f"SELECT name FROM teachers WHERE id={teacher_id[0]}")]
    message = f"Welcome To Course {c_name[0]}".title()
    student_ids = [ s_id[0] for s_id in execute_query(f"SELECT student_id FROM students_courses WHERE course_id={course_id}") ]
    students_names=[]
    for student_id in student_ids:
        student_name = [ s_name[0] for s_name in execute_query(f"SELECT name FROM students WHERE id={student_id}") ]
        students_names.append(student_name[0])
    return render_template("show_course.html", teacher_name=teacher_name, c_name=c_name, message=message, students_names=students_names)



@app.route('/newsletter')
def method_name():
    pass


@app.route('/registrations/<student_id>')
def registrations(student_id):
        # 1. Get course IDs for this student using student_courses
        # 2. Get course names using course IDs
    course_ids=execute_query(f"SELECT course_id FROM students_courses WHERE student_id={student_id}")
    clean_ids=[ c[0] for c in course_ids]
    course_names=[]
    for i in clean_ids:
        course_names.append(execute_query(f"SELECT name FROM courses WHERE id={i}"))
    student_name=execute_query(f"SELECT name FROM students WHERE id={student_id}")
    return render_template("registrations.html", student_name=student_name, course_names=course_names)





# @app.route('/register/<student_id>/<course_id>')
# def register(student_id, course_id):
#     # This endpoint inserts a student into students_courses table so student_id 
#     # is registered to course_id. Then show all courses for this student.
#     execute_query(f"INSERT INTO students_courses VALUES (NULL, '{student_id}', '{course_id}')")
#     return redirect(url_for('registrations', student_id=student_id))
