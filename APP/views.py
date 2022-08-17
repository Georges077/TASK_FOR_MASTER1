# -*- coding: utf-8 -*-
# APP/views.py

""" ეს მოდული გვაწვდის მეთოდებს გამოსახულებასთან სამუშაოდ"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from .model import StudentsModel


class Window(QtWidgets.QMainWindow):
    """მთავარი ფანჯარა"""

    def __init__(self, parent=None):
        """ინიციალიზაცია"""
        super().__init__(parent)
        self.setWindowTitle("სტუდენტების სარეგისტრაციო აპლიკაცია")
        self.resize(1350, 650)
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QtWidgets.QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.stud_model = StudentsModel()
        self.setup_form()

    def setup_form(self):
        """მთავარი ფანჯრის ინიციალიზაცია"""

        """ცხრილის მოწყობა"""
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.stud_model.model)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        """მოქმედებების ღილაკები"""
        self.AddButton = QtWidgets.QPushButton("ჩანაწერის გაკეთება")
        self.AddButton.clicked.connect(self.open_add)
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.setFixedSize(150, 30)
        self.search_field.setPlaceholderText('ძებნის პარამეტრი')
        self.search_field.textChanged.connect(self.stud_model.filter_model.setFilterRegExp)
        self.DeleteButton = QtWidgets.QPushButton("წაშლა")
        self.DeleteButton.clicked.connect(self.delete_student)

        """სტრუქტურის მოწყობა"""
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.AddButton)
        layout.addWidget(self.search_field)
        layout.addWidget(self.DeleteButton)
        layout.addStretch()
        self.table.setModel(self.stud_model.filter_model)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def open_add(self):
        self.dialog = AddForm()
        if self.dialog.exec() == QtWidgets.QDialog.Accepted:
            self.stud_model.add_student(self.dialog.data)

    def delete_student(self):
        """ მონიშნული მონაცემის წაშლის მეთოდი."""
        row = self.table.currentIndex().row()
        if row < 0:
            return
        msg = QtWidgets.QMessageBox.warning(
            self,
            "გაფრთხილება",
            "ნამდვილად გსურთ მონიშნული სტრიქონის წაშლა?",
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )

        if msg == QtWidgets.QMessageBox.Ok:
            self.stud_model.delete_student(row)


class AddForm(QtWidgets.QDialog):
    """ახალი ჩანაწერის გაკეთების ფორმა"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("ჩანაწერის გაკეთება")
        self.layout = QtWidgets.QVBoxLayout()
        self.course_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.f_name = QtWidgets.QLineEdit()
        self.l_name = QtWidgets.QLineEdit()
        self.sub_line_edits = []
        self.sub_point_line_edits = []
        for i in range(5):
            sub_line_edit = QtWidgets.QLineEdit()
            sub_point_line_edit = QtWidgets.QLineEdit()
            self.sub_line_edits.append(sub_line_edit)
            self.sub_point_line_edits.append(sub_point_line_edit)
        self.GPA = QtWidgets.QLineEdit()
        self.buttonsBox = QtWidgets.QDialogButtonBox(self)
        self.group = QtWidgets.QLabel("კურსები")

        self.setup_form()

    def setup_form(self):
        """ფორმის ინიციალიზაციის მეთოდი"""
        self.f_name.setStyleSheet("color:orange; width:200;")
        self.f_name.setPlaceholderText("სახელი")
        self.l_name.setStyleSheet("color:orange; width:200;")
        self.l_name.setPlaceholderText("გვარი")
        self.GPA.setStyleSheet("color:orange; width:200;")
        self.GPA.setPlaceholderText("GPA")
        layout = QtWidgets.QFormLayout()
        stud_layout = QtWidgets.QHBoxLayout()
        stud_layout.addWidget(self.f_name)
        stud_layout.addWidget(self.l_name)
        stud_layout.addWidget(self.GPA)
        layout.addRow(stud_layout)
        for row1, row2 in zip(self.sub_line_edits, self.sub_point_line_edits):
            row1.setStyleSheet("color:orange; width:300;")
            row1.setPlaceholderText("კურსი")
            row2.setStyleSheet("color:orange; width:300;")
            row2.setPlaceholderText("ქულა")
            layout.addRow(row1, row2)

        self.layout.addLayout(layout)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """მონაცემების ვალიდაცია"""
        self.data = []
        self.subjects = []
        for row1, row2 in zip(self.sub_line_edits, self.sub_point_line_edits):
            if row1.text() and row2.text():
                self.subjects.append({f"{row1.text()}": row2.text()})
        for field in (self.f_name, self.l_name, self.GPA):
            if not field.text():
                QtWidgets.QMessageBox.critical(
                    self,
                    "შეცდომა!",
                    f"თქვენ უნდა წარმოადგინოთ სტუდენტის მონაცემები  {field.objectName()}",
                )
                self.data = None
                return

            self.data.append(field.text())

        self.data.append(self.subjects)

        if not self.data:
            return

        super().accept()
