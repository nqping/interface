#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/4 18:07
# @Author  : qingping.niu
# @File    : CreateProjectDialog.py
# @desc    :
import qdarkstyle,sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from utils.globalvar import GlobalVar as gl
from PyQt5.QtWidgets import QTextEdit
from services.ProjectManager import ProjectManager

class CreateProjectDialog(QDialog):
    add_project_success_signal = pyqtSignal()

    def __init__(self,parent=None):
        super(CreateProjectDialog,self).__init__(parent)
        self.userName = gl.get_value("userName")
        self.dbhelper = ProjectManager()
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal) #设置弹框出现后,父窗口不可活动
        self.setWindowTitle("创建项目")



    def setUpUI(self):
        self.resize(300, 250)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.titlelabel = QLabel("创建新项目")
        self.projectNameLabel = QLabel("项目名称:")
        self.remarkLabel = QLabel("备注:")

        # lineEdit控件
        self.projectNameEdit = QLineEdit()
        self.projectNameEdit.setObjectName("projectNameEdit")
        self.projectNameEdit.setPlaceholderText("请输入项目名称")
        self.projectNameEdit.setMaxLength(15)

        self.remarkEdit = QTextEdit()
        self.remarkEdit.setObjectName("remarkEdit")
        self.remarkEdit.setPlaceholderText("请输入项目备注")

        # button控件
        self.submitBtn = QPushButton("提交")
        self.submitBtn.setObjectName("submitBtn")

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)

        font.setPixelSize(14)
        self.projectNameLabel.setFont(font)
        self.remarkLabel.setFont(font)

        # button设置
        font.setPixelSize(16)
        self.submitBtn.setFont(font)
        self.submitBtn.setFixedHeight(32)
        self.submitBtn.setFixedWidth(140)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.projectNameLabel, self.projectNameEdit)
        self.layout.addRow(self.remarkLabel,self.remarkEdit)
        self.layout.addRow("",self.submitBtn)

        QMetaObject.connectSlotsByName(self)


    @pyqtSlot()
    def on_submitBtn_clicked(self):
        #获取数据并验证
        projectName = self.projectNameEdit.text()
        remark = self.remarkEdit.toPlainText()

        if len(projectName) <1 :
            QMessageBox.warning(self,"警告","请输入项目名称")
            return
        #提交数据
        count = self.dbhelper.createProject(projectName=projectName,remark=remark,creator=self.userName)
        if count > 0:
            QMessageBox.information(self, "提示", "项目创建成功!", QMessageBox.Yes, QMessageBox.Yes)
            self.add_project_success_signal.emit()
            self.clearEdit()
            self.close()


    def clearEdit(self):
        self.projectNameEdit.clear()
        self.remarkEdit.clear()



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
#     app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
#     mainMindow = CreateProjectDialog()
#     mainMindow.show()
#     sys.exit(app.exec_())






