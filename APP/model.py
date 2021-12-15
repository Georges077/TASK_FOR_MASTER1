# -*- coding: utf-8 -*-
# APP/model.py

"""ეს მოდული უზრუნველყოფს ბაზის ობიექტებთან ურთიერთობას"""

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtSql import QSqlTableModel


class StudentsModel:
    def __init__(self):
        self.model = self._create_model()
        self.filter_model = self.create_filter_model()

    @staticmethod
    def _create_model():
        """მოდელის შექმნა და მოწყობა"""
        table_model = QSqlTableModel()
        table_model.setTable("students")
        table_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        table_model.select()
        headers = ["id", "fname", "lname", "GPA", "subjects"]
        for columnIndex, header in enumerate(headers):
            table_model.setHeaderData(columnIndex, Qt.Horizontal, header)
        return table_model

    def create_filter_model(self):
        finder = QSortFilterProxyModel()
        finder.setSourceModel(self.model)
        finder.setFilterCaseSensitivity(Qt.CaseInsensitive)
        finder.setFilterKeyColumn(-1)
        return finder

    def add_student(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), str(field))
        self.model.submitAll()
        self.model.select()

    def delete_student(self, row):
        """ წაშლის მეთოდი"""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def search(self, param):
        self.model.find
