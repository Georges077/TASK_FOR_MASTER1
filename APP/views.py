# -*- coding: utf-8 -*-
# APP/views.py

""" ეს მოდული გვაწვდის მეთოდებს გამოსახულებასთან სამუშაოდ"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from  .model import StudentsModel


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
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        """მოქმედებების ღილაკები"""
        self.AddButton = QtWidgets.QPushButton("ჩანაწერის გაკეთება")
        self.AddButton.clicked.connect(self.open_add)
        # self.UpdateButton = QPushButton("ჩანაწერის განახლება")
        self.SearchButton = QtWidgets.QPushButton("ძებნა")
        self.DeleteButton = QtWidgets.QPushButton("წაშლა")

        """სტრუქტურის მოწყობა"""
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.AddButton)
        # layout.addWidget(self.UpdateButton)
        layout.addWidget(self.SearchButton)
        layout.addWidget(self.DeleteButton)
        layout.addStretch()
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def open_add(self):
        self.dialog = AddForm()
        if self.dialog.exec() == QtWidgets.QDialog.Accepted:
            self.stud_model.add_student(self.dialog.data)


class AddForm(QtWidgets.QDialog):
    """ახალი ჩანაწერის გაკეთების ფორმა"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("ჩანაწერის გაკეთება")
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setup_form()

    def setup_form(self):
        self.fname = QtWidgets.QLineEdit()
        self.lname = QtWidgets.QLineEdit()
        self.subjects = QtWidgets.QLineEdit()
        self.GPA = QtWidgets.QLineEdit()

        layout = QtWidgets.QFormLayout()
        layout.addRow("სახელი", self.fname)
        layout.addRow("გვარი", self.lname)
        layout.addRow("კურსი", self.subjects)
        layout.addRow("GPA", self.GPA)

        self.layout.addLayout(layout)
        self.buttonsBox = QtWidgets.QDialogButtonBox(self)
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
        for field in (self.fname, self.lname, self.subjects, self.GPA):
            if not field.text():
                QtWidgets.QMessageBox.critical(
                    self,
                    "შეცდომა!",
                    f"თქვენ უნდა წარმოადგინოთ სტუდენტის მონაცემები  {field.objectName()}",
                )
                self.data = None
                return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()
