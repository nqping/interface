#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/6 15:06
# @Author  : qingping.niu
# @File    : UpdateProjectDialog.py
# @desc    : 修改数据

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from utils.globalvar import GlobalVar as gl
from PyQt5.QtWidgets import QTextEdit
from services.ProjectManager import ProjectManager

class UpdateProjectDialog(QDialog):
    update_project_success_signal = pyqtSignal()

    def __init__(self,projectId=0,projectName=None,remark=None,userName=None,parent=None):
        super(UpdateProjectDialog,self).__init__(parent)
        self.dbhelper = ProjectManager()
        self.projectName = projectName
        self.remark = remark
        self.projectId = projectId
        self.userName = userName
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)  # 设置弹框出现后,父窗口不可活动
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
        self.projectNameEdit.setText(self.projectName)

        self.remarkEdit = QTextEdit()
        self.remarkEdit.setObjectName("remarkEdit")
        self.remarkEdit.setPlaceholderText("请输入项目备注")
        self.remarkEdit.setPlainText(self.remark)

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
        self.layout.addRow(self.remarkLabel, self.remarkEdit)
        self.layout.addRow("", self.submitBtn)

        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_submitBtn_clicked(self):
        # 获取数据并验证
        projectName = self.projectNameEdit.text()
        remark = self.remarkEdit.toPlainText()

        if len(projectName) < 1:
            QMessageBox.information(self, "提示", "请输入项目名称")
            return
        # 提交数据
        count = self.dbhelper.updateByCondition(projectId=self.projectId,projectName=projectName, remark=remark, creator=self.userName)
        if count > 0:
            QMessageBox.information(self, "提示", "项目修改成功!", QMessageBox.Yes, QMessageBox.Yes)
            self.update_project_success_signal.emit()
            self.clearEdit()
            self.close()

    def clearEdit(self):
        self.projectNameEdit.clear()
        self.remarkEdit.clear()
