import sqlite3
from classes import Student, Course, Teacher, User


def query_db(sql_query):
    with sqlite3.connect("students.db") as conn:
        cur = conn.cursor()
        cur.execute(sql_query)
        return cur.fetchall()


def read(table):
    return query_db(f"SELECT * FROM {table}")


def teacher_name(id):
    return query_db(f"SELECT name FROM teachers WHERE id={id}")


def student_name(id):
    return query_db(f"SELECT name FROM students WHERE id={id}")


def read_where(values, table, column, value):
    return query_db(f"SELECT {values} FROM {table} WHERE {column}={value}")


def read_whereX2(values, table, column0, value0, column1, value1):
    return query_db(f"SELECT {values} FROM {table} WHERE {column0}={value0} AND {column1}={value1}")


def read_by_like(values, table, column, search):
    return query_db(f"SELECT {values} FROM {table} WHERE {column} LIKE '%{search}%'")


def insert(table, columns, values):
    query_db(f"INSERT INTO {table} ({columns}) VALUES ({values})")


def delete(table, task_id):
    query_db(f"DELETE FROM {table} WHERE id={task_id}")


def update_attend(table, column0, value0, column1, value1, column2, value2, column3, value3):
    query_db(f"UPDATE {table} SET {column0}={value0} WHERE {column1}={value1} AND {column2}={value2} AND {column3}={value3};")
