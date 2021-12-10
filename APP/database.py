# -*- coding: utf-8 -*-
# APP/database.py
"""ეს მოდული უზრუნველყოფს ბაზასთან ურთიერთობას"""

from  PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def create_connection(databaseName):
    """ბაზასთან კავშირი"""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "სტუდენტი",
            f"ბაზის შეცდომა: {connection.lastError().text()}"
        )
        return False
    create_students_table()
    return True

def create_students_table():
    """სტუდენტტების ცხრილის შექმნა"""
    create_table_query = QSqlQuery()
    return create_table_query.exec(
        """CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
            fname VARCHAR(40) NOT NULL, 
            lname VARCHAR(40) NOT NULL, 
            subjects JSON[], 
            GPA INTEGER
            )"""
    )
