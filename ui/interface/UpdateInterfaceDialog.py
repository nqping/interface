#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/8 10:39
# @Author  : qingping.niu
# @File    : UpdateInterfaceDialog.py
# @desc    :

import datetime,sys
from services.InterfaceManager import InterfaceManager
from model.Interface import Interface
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from utils.globalvar import GlobalVar as gl

class UpdateInterfaceDialog(QDialog):
    update_interface_success_signal = pyqtSignal()

    def __init__(self,list=[]):
        super(UpdateInterfaceDialog,self).__init__()
        self.dbhelper = InterfaceManager()
        if list != [] :
            self.obj = Interface()
            self.obj.faceId = list[0]
            self.obj.faceName = list[1]
            self.obj.address = list[2]
            self.obj.requestType = list[3]
            self.obj.dataType = list[4]
            self.obj.contentType = list[5]
            self.obj.caseCount = list[6]
            self.obj.projectName = list[8]
            self.obj.projectId = list[9]
            self.obj.userId = list[10]

        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)  # 设置弹框出现后,父窗口不可活动
        self.setWindowTitle("修改接口")


    def setUpUI(self):
        self.resize(550, 250)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # 设置字体
        font = QFont()
        font.setPixelSize(14)

        # label控件<font color=#FF0000>*</font>
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

        rsData = self.dbhelper.getProjectName()
        self.projectBox = QComboBox()
        for data in rsData:
            self.projectBox.addItem(str(data[1]), str(data[0]))

        self.projectBox.setFixedHeight(35)
        self.projectBox.setFont(font)
        self.projectBox.setCurrentText(self.obj.projectName)

        self.faceNameEdit = QLineEdit()
        self.faceNameEdit.setObjectName("faceNameEdit")
        self.faceNameEdit.setPlaceholderText("输入接口名称")
        self.faceNameEdit.setFixedHeight(35)
        self.faceNameEdit.setFont(font)
        self.faceNameEdit.setText(self.obj.faceName)

        self.addressEdit = QLineEdit()
        self.addressEdit.setObjectName("addressEdit")
        self.addressEdit.setPlaceholderText("输入接口地址")
        self.addressEdit.setFixedHeight(35)
        self.addressEdit.setFont(font)
        self.addressEdit.setText(self.obj.address)

        self.requestTypeBox = QComboBox()
        self.requestTypeBox.setObjectName("requestTypeBox")
        requestTypeData = ["POST", "GET", "PUT", "DELETE", "PATCH", "HEAD", "OPTION"]
        self.requestTypeBox.addItems(requestTypeData)
        self.requestTypeBox.setFixedHeight(35)
        self.requestTypeBox.setFont(font)
        self.requestTypeBox.setCurrentText(self.obj.requestType)

        self.dataTypeBox = QComboBox()
        self.dataTypeBox.setObjectName("dataTypeBox")
        dataTypeData = ["json", "xml", "text", "script", "jsonp"]
        self.dataTypeBox.addItems(dataTypeData)
        self.dataTypeBox.setFixedHeight(35)
        self.dataTypeBox.setFont(font)
        self.dataTypeBox.setCurrentText(self.obj.dataType)

        self.contentTypeEdit = QLineEdit()
        self.contentTypeEdit.setObjectName("contentTypeEdit")
        self.contentTypeEdit.setPlaceholderText("例如:application/json")
        self.contentTypeEdit.setFixedHeight(35)
        self.contentTypeEdit.setFont(font)
        self.contentTypeEdit.setText(self.obj.contentType)

        # button设置
        font.setPixelSize(16)
        # button控件
        self.updateBtn = QPushButton("修 改")
        self.updateBtn.setObjectName("updateBtn")
        self.updateBtn.setFont(font)
        self.updateBtn.setFixedHeight(32)
        self.updateBtn.setFixedWidth(140)

        # 添加进formlayout
        self.layout.addRow(projectLabel, self.projectBox)
        self.layout.addRow(nameLabel, self.faceNameEdit)
        self.layout.addRow(addressLabel, self.addressEdit)
        self.layout.addRow(requestTypeLabel, self.requestTypeBox)
        self.layout.addRow(contentTypeLabel, self.contentTypeEdit)
        self.layout.addRow("", self.updateBtn)

        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def on_updateBtn_clicked(self):
        projectId = self.projectBox.currentData()
        projectName = self.projectBox.currentText()
        requestType = self.requestTypeBox.currentText()
        dataType = self.dataTypeBox.currentText()
        contentType = self.contentTypeEdit.text()
        faceName = self.faceNameEdit.text()
        address = self.addressEdit.text()
        if faceName == "" or address == "":
            QMessageBox.warning(self, "警告", " * 号参数必须填空", QMessageBox.Yes, QMessageBox.Yes)
            return

        self.obj.faceName = faceName
        self.obj.address = address
        self.obj.projectId = projectId
        self.obj.projectName = projectName
        self.obj.requestType = requestType
        self.obj.dataType = dataType
        self.obj.contentType = contentType
        self.obj.createTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # obj.userId = self.obj.userId
        # obj.caseCount = self.obj.caseCount
        # obj.faceId = self.obj.faceId

        count = self.dbhelper.updateInterface(self.obj)
        if count > 0:
            QMessageBox.information(self,"提示","修改成功")
            self.update_interface_success_signal.emit()
            self.close()
            self.clearEdit()

    def clearEdit(self):
        self.faceNameEdit.clear()
        self.addressEdit.clear()
        self.contentTypeEdit.clear()

    # ['171', '测试2', 'createinterfacedialog', 'POST', 'json', '5555', '0', '2019-01-08 14:08:50', 'JoyLockscreen', '6',
    #  'None']


# if __name__ == "__main__":
#     list =  ['171', '测试2', 'createinterfacedialog', 'POST', 'json', '5555', '0', '2019-01-08 14:08:50', 'JoyLockscreen', '6','None']
#     app = QApplication(sys.argv)
#     app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
#     # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
#     mainMindow = UpdateInterfaceDialog(list)
#     mainMindow.show()
#     sys.exit(app.exec_())
