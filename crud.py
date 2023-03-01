import sqlite3
from classes import Student, Course, Teacher, User


def query_db(sql_query):
    with sqlite3.connect("students.db") as conn:
        cur = conn.cursor()
        cur.execute(sql_query)
        return cur.fetchall()


def insert_students(name, email, phone):
    query_db(f"INSERT INTO students VALUES (NULL, '{name}', '{email}', '{phone}');")


def insert_teachers(name, email):
    query_db(f"INSERT INTO teachers VALUES (NULL, '{name}', '{email}');")


def insert_users(email, password, role):
    query_db(f"INSERT INTO users VALUES (NULL, '{email}', '{password}', '{role}');")


def insert_students_courses(s_id, c_id, grade):
    query_db(f"INSERT INTO students_courses VALUES (NULL, '{s_id}', '{c_id}', '{grade}');")


def read(table):
    return query_db(f"SELECT * FROM {table}")


def read_by_id(table, id):
    return query_db(f"SELECT * FROM {table} WHERE id={id}")


def read_by_name(table, name):
    return query_db(f"SELECT * FROM {table} WHERE name='{name}'")


def read_by_like(table, search):
    return query_db(f"SELECT * FROM {table} WHERE name LIKE '%{search}%'")


def delete(table, task_id):
    query_db(f"DELETE FROM {table} WHERE id={task_id}")


def update_description(table, name, description, date, task_id):
    query_db(f"UPDATE {table} SET name='{name}', description='{description}', date='{date}' WHERE id={task_id};")
