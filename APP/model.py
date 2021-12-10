# -*- coding: utf-8 -*-
# APP/model.py

"""ეს მოდული უზრუნველყოფს ბაზის ობიექტებთან ურთიერთობას"""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

class StudentsModel:
    def __init__(self):
        self.model= self._create_model()

    @staticmethod
    def _create_model():
        """მოდელის შექმნა და მოწყობა"""
        table_model = QSqlTableModel()
        table_model.setTable("students")
        table_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        table_model.select()
        headers = ["id", "fname", "lname", "subjects", "GPA"]
        for columnIndex, header in enumerate(headers):
            table_model.setHeaderData(columnIndex, Qt.Horizontal, header)
        return table_model

    def add_student(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()
