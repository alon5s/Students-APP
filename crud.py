import sqlite3
from classes import Student, Course, Teacher, User


def query_db(sql_query):
    with sqlite3.connect("students.db") as conn:
        cur = conn.cursor()
        cur.execute(sql_query)
        return cur.fetchall()


def read(table):
    return query_db(f"SELECT * FROM {table}")


def read_where(values, table, column, value):
    return query_db(f"SELECT {values} FROM {table} WHERE {column}={value}")


def read_by_like(values, table, column, search):
    return query_db(f"SELECT {values} FROM {table} WHERE {column} LIKE '%{search}%'")


def insert(table, columns, values):
    query_db(f"INSERT INTO {table} ({columns}) VALUES ({values})")


def delete(table, task_id):
    query_db(f"DELETE FROM {table} WHERE id={task_id}")


def update(table, column, value, description, date, task_id):
    query_db(f"UPDATE {table} SET {column}='{value}', description='{description}', date='{date}' WHERE id={task_id};")
