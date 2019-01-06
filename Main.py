#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 14:45
# @Author  : qingping.niu
# @File    : Main.py
# @desc    : 程序入口

import sys

import qdarkstyle
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *

from ui.MainWindow import Main

if __name__ == "__main__":
    app = QApplication(sys.argv) #qdarkstyle.load_stylesheet_pyqt5()
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = Main()
    mainMindow.show()
    sys.exit(app.exec_())

