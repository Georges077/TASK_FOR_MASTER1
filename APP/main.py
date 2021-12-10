# -*- coding: utf-8 -*-
# APP/main.py

""" აპლიკაციიის მთავარი ინსტანცია. """

import sys

from PyQt5.QtWidgets import QApplication
from .views import Window
from .database import create_connection


def main():
    app = QApplication(sys.argv)
    if not create_connection("students.sqlite"):
        sys.exit(1)
    win = Window()
    win.show()
    sys.exit(app.exec())
