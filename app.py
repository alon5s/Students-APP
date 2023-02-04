from flask import Flask,request,redirect,url_for,render_template
app = Flask(__name__)
from setup_db import execute_query

@app.route('/')
def home():
    return render_template("index.html")

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

@app.route('/course_list')
def search():
    courses = execute_query("SELECT * FROM courses")
    return render_template("course_list.html", courses=courses)

@app.route('/course/<course_id>')
def show_course(course_id):
    course_name = [ c[0] for c in execute_query(f"SELECT name FROM courses WHERE id={course_id}") ]
    teacher_id = [ t_id[0] for t_id in execute_query(f"SELECT teacher_id FROM courses WHERE id={course_id}") ]
    teacher_name = [ t_name[0] for t_name in execute_query(f"SELECT name FROM teachers WHERE id={teacher_id[0]}")]
    message = f"Welcome To Course {course_name[0]}".title()
    student_ids = [ s_id[0] for s_id in execute_query(f"SELECT student_id FROM students_courses WHERE course_id={course_id}") ]
    students_names=[]
    for student_id in student_ids:
        student_name = [ s_name[0] for s_name in execute_query(f"SELECT name FROM students WHERE id={student_id}") ]
        students_names.append(student_name[0])
    return render_template("show_course.html", teacher_name=teacher_name, course_name=course_name, message=message, students_names=students_names)

@app.route('/lists')
def lists():
    students = execute_query("SELECT * FROM students")
    teachers = execute_query("SELECT * FROM teachers")
    courses = execute_query("SELECT * FROM courses")
    return render_template("lists.html", students=students, teachers=teachers, courses=courses)



@app.route('/register/<student_id>/<course_id>')
def register(student_id, course_id):
        # This endpoint inserts a student into students_courses table so student_id 
        # is registered to course_id. Then show all courses for this student.
    execute_query(f"INSERT INTO students_courses VALUES (NULL, '{student_id}', '{course_id}')")
    return redirect(url_for('registrations', student_id=student_id))

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