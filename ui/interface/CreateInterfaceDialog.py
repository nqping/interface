#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/8 10:39
# @Author  : qingping.niu
# @File    : CreateInterfaceDialog.py
# @desc    : 新增接口

import qdarkstyle,sys,datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from services.InterfaceManager import InterfaceManager
from utils.globalvar import GlobalVar as gl
from model.Interface import Interface



class CreateInterfaceDialog(QDialog):
    add_interface_success_signal = pyqtSignal()

    def __init__(self):
        super(CreateInterfaceDialog,self).__init__()
        self.userId = gl.get_value("userId")
        self.dbhelper = InterfaceManager()
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)  # 设置弹框出现后,父窗口不可活动
        self.setWindowTitle("新增接口")

    def setUpUI(self):
        self.resize(550, 250)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # 设置字体
        font = QFont()
        font.setPixelSize(14)

        #label控件<font color=#FF0000>*</font>
        projectLabel = QLabel("项   目:<font color=#FF0000>*</font>")
        nameLabel = QLabel("接口名称:<font color=#FF0000>*</font>")
        addressLabel = QLabel("地   址:<font color=#FF0000>*</font>")
        requestTypeLabel = QLabel("请求方式:<font color=#FF0000>*</font>")
        dataTypeLabel = QLabel("数据格式:<font color=#FF0000>*</font>")
        contentTypeLabel = QLabel("Content-Type:")

        projectLabel.setFont(font)
        nameLabel.setFont(font)
        addressLabel.setFont(font)
        requestTypeLabel.setFont(font)
        dataTypeLabel.setFont(font)
        contentTypeLabel.setFont(font)

        # lineEdit控件
        rsData = self.dbhelper.getProjectName()
        self.projectBox = QComboBox()
        for data in rsData:
            self.projectBox.addItem(str(data[1]), str(data[0]))

        self.projectBox.setFixedHeight(35)
        self.projectBox.setFont(font)


        self.faceNameEdit = QLineEdit()
        self.faceNameEdit.setObjectName("faceNameEdit")
        self.faceNameEdit.setPlaceholderText("输入接口名称")
        self.faceNameEdit.setFixedHeight(35)
        self.faceNameEdit.setFont(font)

        self.addressEdit = QLineEdit()
        self.addressEdit.setObjectName("addressEdit")
        self.addressEdit.setPlaceholderText("输入接口地址")
        self.addressEdit.setFixedHeight(35)
        self.addressEdit.setFont(font)

        self.requestTypeBox = QComboBox()
        self.requestTypeBox.setObjectName("requestTypeBox")
        requestTypeData=["POST","GET","PUT","DELETE","PATCH","HEAD","OPTION"]
        self.requestTypeBox.addItems(requestTypeData)
        self.requestTypeBox.setFixedHeight(35)
        self.requestTypeBox.setFont(font)

        self.dataTypeBox = QComboBox()
        self.dataTypeBox.setObjectName("dataTypeBox")
        dataTypeData=["json","xml","text","script","jsonp"]
        self.dataTypeBox.addItems(dataTypeData)
        self.dataTypeBox.setFixedHeight(35)
        self.dataTypeBox.setFont(font)

        self.contentTypeEdit = QLineEdit()
        self.contentTypeEdit.setObjectName("contentTypeEdit")
        self.contentTypeEdit.setPlaceholderText("例如:application/json")
        self.contentTypeEdit.setFixedHeight(35)
        self.contentTypeEdit.setFont(font)

        # button设置
        font.setPixelSize(16)
        # button控件
        self.submitBtn = QPushButton("添 加")
        self.submitBtn.setObjectName("submitBtn")
        self.submitBtn.setFont(font)
        self.submitBtn.setFixedHeight(32)
        self.submitBtn.setFixedWidth(140)

        # 添加进formlayout
        self.layout.addRow(projectLabel,self.projectBox)
        self.layout.addRow(nameLabel,self.faceNameEdit)
        self.layout.addRow(addressLabel,self.addressEdit)
        self.layout.addRow(requestTypeLabel,self.requestTypeBox)
        self.layout.addRow(contentTypeLabel,self.contentTypeEdit)
        self.layout.addRow("",self.submitBtn)

        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_submitBtn_clicked(self):
        projectId = self.projectBox.currentData()
        projectName = self.projectBox.currentText()
        requestType = self.requestTypeBox.currentText()
        dataType = self.dataTypeBox.currentText()
        contentType = self.contentTypeEdit.text()
        faceName = self.faceNameEdit.text()
        address = self.addressEdit.text()
        if faceName == "" or address == "":
            QMessageBox.warning(self,"警告"," * 号参数必须填空", QMessageBox.Yes, QMessageBox.Yes)
            return
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        obj = Interface()
        obj.faceName = faceName
        obj.address = address
        obj.projectId = projectId
        obj.projectName = projectName
        obj.requestType = requestType
        obj.dataType = dataType
        obj.contentType = contentType
        obj.createTime = now_time
        obj.userId = self.userId

        count = self.dbhelper.addInterface(obj)
        if count > 0:
            QMessageBox.information(self,"提示","接口添加成功",QMessageBox.Yes, QMessageBox.Yes)
            self.add_interface_success_signal.emit()
            self.close()
            self.clearEdit()

    def clearEdit(self):
        self.faceNameEdit.clear()
        self.addressEdit.clear()
        self.contentTypeEdit.clear()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = CreateInterfaceDialog()
    mainMindow.show()
    sys.exit(app.exec_())

