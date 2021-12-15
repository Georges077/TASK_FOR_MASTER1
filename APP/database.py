# -*- coding: utf-8 -*-
# APP/database.py
"""ეს მოდული უზრუნველყოფს ბაზასთან ურთიერთობას"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord



def create_connection(databaseName):
    """ბაზასთან კავშირი"""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName("students.sqlite")

    if not connection.open():
        QMessageBox.warning(
            None,
            "სტუდენტი",
            f"ბაზის შეცდომა: {connection.lastError().text()}"
        )
        return False
    create_students_table()
    insert_students_from_file()
    return True

def create_students_table():
    """სტუდენტების ცხრილის შექმნა"""
    create_table_query = QSqlQuery()
    return create_table_query.exec(
        """CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
            fname VARCHAR(40) NOT NULL, 
            lname VARCHAR(40) NOT NULL, 
            GPA INTEGER,
            subjects JSON[] 
        )"""
    )


def insert_students_from_file():
    """ პირველადი მონაცემების ჩაწერა"""
    with open("APP/students.in", 'r') as st:
        insert_query = QSqlQuery()
        insert_query.exec_(f""" SELECT * FROM students;""")
        if insert_query.next():
            return True
        print("inserting data...")
        for row in st.readlines():
            student = []
            course = '['
            r = row.split('#')
            student.append(r[1])
            student.append(r[0])
            student.append(r[len(r) - 1:][0].replace('\n', ''))
            for i in range(0, len(r[2:-1]), 2):
                if i+1 < len(r[2:-1]):
                    course += "{" + f"'{r[2:-1][i]}': '{r[2:-1][i + 1]}'" + "},"
                course += ']'
                student.append(course)
                insert_query.prepare(f""" INSERT INTO students(fname, lname, GPA, subjects) VALUES  (?, ?, ?, ?)""")
                insert_query.addBindValue(student[0])
                insert_query.addBindValue(student[1])
                insert_query.addBindValue(student[2])
                insert_query.addBindValue(student[3])
                if not insert_query.exec():
                    print(insert_query.lastError().text())
                    return False
    print("inserted data.")
    return True
