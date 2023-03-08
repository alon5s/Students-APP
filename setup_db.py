import sqlite3
import faker
import random


def execute_query(sql):
    with sqlite3.connect("students.db") as conn:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()


def create_tables():
    execute_query("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            teacher_id TEXT NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS students_courses (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            course_id INTEGER,
            grade INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id),
            UNIQUE (student_id, course_id)
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            FOREIGN KEY (email) REFERENCES students (email)
        )
    """)
    execute_query("""
    CREATE TABLE IF NOT EXISTS attendances (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        date TEXT,
        attendance TEXT,
        UNIQUE (student_id, course_id, date),
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (id)
    )
    """)


def create_fake_data(students_num=40, teachers_num=4):
    fake = faker.Faker()
    default_password = 12345678
    i = 0
    for student in range(students_num):
        i += 1
        execute_query(f"""INSERT INTO students_courses (student_id,course_id,grade) VALUES ({i},{random.randint(1,4)},{random.randint(55,100)})""")
    for student in range(students_num):
        student = {"name": fake.name(), "email": fake.email()}
        execute_query(f"""INSERT INTO students (name,email) VALUES ('{student["name"]}','{student["email"]}')""")
        execute_query(f"""INSERT INTO users (email,password,role) VALUES ('{student["email"]}','{default_password}','student')""")
    for teacher in range(teachers_num):
        teacher = {"name": fake.name(), "email": fake.email()}
        execute_query(f"""INSERT INTO teachers (name,email) VALUES ('{teacher["name"]}','{teacher["email"]}')""")
        execute_query(f"""INSERT INTO users (email,password,role) VALUES ('{teacher["email"]}','{default_password}','teacher')""")
    courses = ['python', 'javascript', 'html', 'css']
    for course_name in courses:
        teacher_ids = [tup[0] for tup in execute_query("SELECT id FROM teachers")]
        execute_query(f"INSERT INTO courses (name, teacher_id) VALUES ('{course_name}','{random.choice(teacher_ids)}')")
    execute_query("INSERT INTO users VALUES (NULL,'admin@admin.com','admin','admin')")


if __name__ == "__main__":
    create_tables()
    create_fake_data()
