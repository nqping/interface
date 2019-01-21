#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 16:57
# @Author  : qingping.niu
# @File    : UpdateCaseDialog.py
# @desc    :

import datetime,sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTextEdit
from services.CaseManager import CaseManager
from utils.md5Utils import md5Encode
from utils.log import LOG
from model.Cases import Cases


keyList=[]

class UpdateCaseDialog(QDialog):
    update_case_success_signal = pyqtSignal()

    def __init__(self,case=None):
        super(UpdateCaseDialog,self).__init__()
        self.dbhelper = CaseManager()
        self.obj = case
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)  # 设置弹框出现后,父窗口不可活动
        self.setWindowTitle("修改接口")

        if self.obj.request is not None:
            self.update_request_table(self.obj.request)

        if self.obj.pretreat is not None:
            self.update_pretreat_table(self.obj.pretreat)

    def setUpUI(self):
        self.resize(650, 700)
        self.formlayout = QFormLayout() #表单布局
        self.vboxlayout = QVBoxLayout() #重布局
        self.mainHboxLayout = QVBoxLayout() #水平布局
        self.setLayout(self.mainHboxLayout)

        # 设置字体
        font = QFont()
        font.setPixelSize(14)
        caseNameLabel = QLabel("用例名:")
        testPointLabel = QLabel("测试点:")
        httpStatusLabel = QLabel("请求状态")

        caseNameLabel.setFont(font)
        testPointLabel.setFont(font)
        httpStatusLabel.setFont(font)

        self.caseNameEdit = QLineEdit()
        self.caseNameEdit.setObjectName("caseNameEdit")
        self.caseNameEdit.setPlaceholderText("输入测试名称")
        self.caseNameEdit.setFixedHeight(30)
        self.caseNameEdit.setFont(font)
        self.caseNameEdit.setText(self.obj.casename)

        self.testPointEdit = QLineEdit()
        self.testPointEdit.setObjectName("testPointEdit")
        self.testPointEdit.setPlaceholderText("输入测试点")
        self.testPointEdit.setFixedHeight(30)
        self.testPointEdit.setFont(font)
        self.testPointEdit.setText(self.obj.testpoint)

        self.httpStatusEdit = QLineEdit()
        self.httpStatusEdit.setObjectName("httpStatusEdit")
        self.httpStatusEdit.setPlaceholderText("http请求状态:200")
        self.httpStatusEdit.setFixedHeight(35)
        self.httpStatusEdit.setFont(font)
        self.httpStatusEdit.setText(self.obj.httpstatus)

        font.setPixelSize(16)
        # button控件
        self.updateSubmitBtn = QPushButton("提交")
        self.updateSubmitBtn.setObjectName("updateSubmitBtn")
        self.updateSubmitBtn.setFont(font)
        self.updateSubmitBtn.setFixedHeight(32)
        self.updateSubmitBtn.setFixedWidth(140)

        # self.clearBtn = QPushButton("重置")
        # self.clearBtn.setObjectName("clearBtn")
        # self.clearBtn.setFont(font)
        # self.clearBtn.setFixedHeight(32)
        # self.clearBtn.setFixedWidth(140)

        self.tabwidget = QTabWidget()
        self.tabwidget.setObjectName("tabwidget")
        self.tabwidget.setFont(font)
        self.tab_pretreat_params()  # 前置处理
        self.tab_request_params()  # 请求参数
        self.tab_expected_params()  # 预期结果
        self.tab_postposition_params()  # 后置处理
        # self.tabwidget.currentChanged.connect(self.changeTab)

        self.vboxlayout.addWidget(self.tabwidget)

        myHbox = QHBoxLayout()
        myHbox.addWidget(self.updateSubmitBtn)
        # myHbox.addWidget(self.clearBtn)

        self.formlayout.addRow(caseNameLabel, self.caseNameEdit)
        self.formlayout.addRow(testPointLabel, self.testPointEdit)
        self.formlayout.addRow(httpStatusLabel, self.httpStatusEdit)

        self.mainHboxLayout.addLayout(self.formlayout)
        self.mainHboxLayout.addLayout(self.vboxlayout)
        self.mainHboxLayout.addLayout(myHbox)

        QMetaObject.connectSlotsByName(self)

    def update_request_table(self,reDict):
        # reDict = self.obj.request
        dict = eval(reDict) #转换字典
        temptuple = dict.items() #返回元组数组
        count=0
        for key,value in temptuple:

            if key == "sign":
                break

            row = self.reTableView.rowCount()  # 获取行数
            self.reTableView.insertRow(row)  # 在末尾插入一空行
            checkbox = QCheckBox()
            if key in self.obj.keylist:
                checkbox.setChecked(True)

            keyEdit = QLineEdit()
            keyEdit.setPlaceholderText("参数名")
            keyEdit.setText(key)

            valueEdit = QLineEdit()
            valueEdit.setPlaceholderText("值")
            valueEdit.setText(value)

            delRowBtn0 = QPushButton()
            delRowBtn0.setIcon(QIcon("../../images/117.png"))
            delRowBtn0.setFixedHeight(25)
            delRowBtn0.setFixedWidth(30)
            delRowBtn0.clicked.connect(self.deleteRow_pretreat)

            self.reTableView.setCellWidget(count, 0, checkbox)
            self.reTableView.setCellWidget(count, 1, keyEdit)
            self.reTableView.setCellWidget(count, 2, valueEdit)
            self.reTableView.setCellWidget(count, 3, delRowBtn0)
            count += 1


    def update_pretreat_table(self,preDict):
        # preDict = self.obj.pretreat
        dict = eval(preDict)  # 转换字典
        temptuple = dict.items()  # 返回元组数组
        count = 0
        for key, value in temptuple:
            row = self.preTableView.rowCount()  # 获取行数
            self.preTableView.insertRow(row)  # 在末尾插入一空行

            keyEdit = QLineEdit()
            keyEdit.setPlaceholderText("参数名")
            keyEdit.setText(key)

            valueEdit = QLineEdit()
            valueEdit.setPlaceholderText("值")
            valueEdit.setText(value)

            delRowBtn = QPushButton()
            delRowBtn.setIcon(QIcon("../../images/117.png"))
            delRowBtn.setFixedHeight(25)
            delRowBtn.setFixedWidth(30)
            delRowBtn.clicked.connect(self.deleteRow_pretreat)

            self.preTableView.setCellWidget(count, 0, keyEdit)
            self.preTableView.setCellWidget(count, 1, valueEdit)
            self.preTableView.setCellWidget(count, 2, delRowBtn)
            count += 1

    def tab_pretreat_params(self):
        '''前置处理'''
        formlayout = QFormLayout()
        vboxlayout = QVBoxLayout()

        addRowBtn = QPushButton()
        addRowBtn.setIcon(QIcon("../images/112.png"))
        addRowBtn.setFixedHeight(30)
        addRowBtn.setFixedWidth(30)

        addRowBtn.clicked.connect(self.insertRow_pretreat)

        self.preTableView = QTableWidget(0, 3)
        self.preTableView.setHorizontalHeaderLabels(["参数名", "值", "操作"])
        self.preTableView.setShowGrid(True)
        self.preTableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格整行选中
        # self.preTableView.horizontalHeader().resizeSection(0, 80)
        self.preTableView.horizontalHeader().resizeSection(0, 150)
        self.preTableView.horizontalHeader().resizeSection(1, 250)
        self.preTableView.horizontalHeader().resizeSection(2, 50)

        formlayout.addRow(addRowBtn)
        vboxlayout.addLayout(formlayout)
        vboxlayout.addWidget(self.preTableView)

        widget = QWidget()
        widget.setLayout(vboxlayout)
        self.tabwidget.addTab(widget, "前置处理")

    def tab_request_params(self):
        '''请求参数'''
        formlayout1 = QFormLayout()
        vboxlayout1 = QVBoxLayout()

        self.reTableView = QTableWidget(0, 4)
        self.reTableView.setHorizontalHeaderLabels(["是否签名", "参数名", "值", "操作"])
        self.reTableView.setShowGrid(True)
        self.reTableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格整行选中

        addRowBtn = QPushButton()
        addRowBtn.setIcon(QIcon("../../images/112.png"))
        addRowBtn.setFixedHeight(30)
        addRowBtn.setFixedWidth(30)
        addRowBtn.clicked.connect(self.insertRow_request)

        self.signLabel = QLabel("")
        self.signLabel.setText("签名顺序:%s"%self.obj.keylist)

        self.reTableView.horizontalHeader().resizeSection(0, 80)  # 重置列宽
        self.reTableView.horizontalHeader().resizeSection(1, 150)
        self.reTableView.horizontalHeader().resizeSection(2, 250)
        self.reTableView.horizontalHeader().resizeSection(3, 50)

        formlayout1.addRow(addRowBtn, self.signLabel)
        vboxlayout1.addLayout(formlayout1)
        vboxlayout1.addWidget(self.reTableView)

        widget = QWidget()
        widget.setLayout(vboxlayout1)
        self.tabwidget.addTab(widget, "请求参数")

    def tab_expected_params(self):
        '''预期结果'''
        vboxlayout1 = QVBoxLayout()

        font = QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        self.expectedEdit = QTextEdit()
        self.expectedEdit.setFont(font)

        self.expectedEdit.setPlainText(self.obj.expected)
        vboxlayout1.addWidget(self.expectedEdit)
        widget = QWidget()
        widget.setLayout(vboxlayout1)
        self.tabwidget.addTab(widget, "预期结果")

    def tab_postposition_params(self):
        '''后置处理'''
        vboxlayout1 = QVBoxLayout()
        font = QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)

        self.postpositionEdit = QTextEdit()
        self.postpositionEdit.setFont(font)
        self.postpositionEdit.setPlainText(self.obj.postposition)
        vboxlayout1.addWidget(self.postpositionEdit)
        widget = QWidget()
        widget.setLayout(vboxlayout1)
        self.tabwidget.addTab(widget, "后置处理")

    def insertRow_request(self):
        '''添加行(请求参数)'''
        row = self.reTableView.rowCount()  # 获取行数
        self.reTableView.insertRow(row)  # 在末尾插入一空行

        checkbox = QCheckBox()
        checkbox.stateChanged.connect(lambda: self.checkboxState(checkbox))

        keyEdit = QLineEdit()
        keyEdit.setPlaceholderText("参数名")
        valueEdit = QLineEdit()
        valueEdit.setPlaceholderText("值")

        delRowBtn = QPushButton()
        delRowBtn.setIcon(QIcon("../../images/117.png"))
        delRowBtn.setFixedHeight(25)
        delRowBtn.setFixedWidth(30)
        delRowBtn.clicked.connect(self.deleteRow_request)

        self.reTableView.setCellWidget(row, 0, checkbox)
        self.reTableView.setCellWidget(row, 1, keyEdit)
        self.reTableView.setCellWidget(row, 2, valueEdit)
        self.reTableView.setCellWidget(row, 3, delRowBtn)

    def checkboxState(self, checkbox):
        row = self.reTableView.currentRow()
        if checkbox.isChecked():
            signkey = self.reTableView.cellWidget(row, 1).text()
            keyList.append(signkey)
            self.signLabel.setText("签名顺序:" + str(keyList))
        else:
            signkey = self.reTableView.cellWidget(row, 1).text()
            if signkey in keyList:
                keyList.remove(signkey)

            self.signLabel.setText("签名顺序:" + str(keyList))

    def deleteRow_request(self):
        '''删除行(请求参数)'''
        row = self.reTableView.currentRow()  # 获取当前行
        # del_d = self.reTableView.cellWidget(row, 1).text()
        self.reTableView.removeRow(row)  # 删除行

    def deleteRow_pretreat(self):
        '''删除行(前置参数)'''
        row = self.preTableView.currentRow()
        # ss = self.preTableView.cellWidget(row, 1).text()
        self.preTableView.removeRow(row)

    def insertRow_pretreat(self):
        '''插入行(前置参数)'''
        row = self.preTableView.rowCount()  # 获取行数
        self.preTableView.insertRow(row)  # 在末尾插入一空行

        keyEdit = QLineEdit()
        keyEdit.setPlaceholderText("参数名")
        valueEdit = QLineEdit()
        valueEdit.setPlaceholderText("值")

        delRowBtn0 = QPushButton()
        delRowBtn0.setIcon(QIcon("../../images/117.png"))
        delRowBtn0.setFixedHeight(25)
        delRowBtn0.setFixedWidth(30)
        delRowBtn0.clicked.connect(self.deleteRow_pretreat)

        # self.preTableView.setCellWidget(row, 0, QCheckBox())
        self.preTableView.setCellWidget(row, 0, keyEdit)
        self.preTableView.setCellWidget(row, 1, valueEdit)
        self.preTableView.setCellWidget(row, 2, delRowBtn0)

    @pyqtSlot()
    def checkboxState(self, checkbox):
        row = self.reTableView.currentRow()
        if checkbox.isChecked():
            signkey = self.reTableView.cellWidget(row, 1).text()
            keyList.append(signkey)
            self.signLabel.setText("签名顺序:" + str(keyList))
        else:
            signkey = self.reTableView.cellWidget(row, 1).text()
            if signkey in keyList:
                keyList.remove(signkey)

            self.signLabel.setText("签名顺序:" + str(keyList))

    @pyqtSlot()
    def on_updateSubmitBtn_clicked(self):
        caseName = self.caseNameEdit.text()
        testPoint = self.testPointEdit.text()
        httpStatus = self.httpStatusEdit.text()
        # 前置处理
        preDict = {}
        rowCount = self.preTableView.rowCount()
        for i in range(rowCount):
            key = self.preTableView.cellWidget(i, 0).text()
            value = self.preTableView.cellWidget(i, 1).text()
            preDict.setdefault(key, value)

        # 请求参数
        reqestDict = {}
        rowCount = self.reTableView.rowCount()
        for i in range(rowCount):
            key = self.reTableView.cellWidget(i, 1).text()
            value = self.reTableView.cellWidget(i, 2).text()
            reqestDict.setdefault(key, value)

        # 预期结果
        expected = self.expectedEdit.toPlainText()
        # 后置处理
        postposition = self.postpositionEdit.toPlainText()

        # 获取签名
        temp = []
        signvalue =""
        if len(keyList) > 0 and keyList != []:
            for mykey in keyList:
                val = reqestDict.get(mykey)
                temp.append(val)
            signvalue = md5Encode(temp)

        LOG.info('签名:%s,%s'%(keyList,signvalue))

        self.obj.casename = caseName
        self.obj.testpoint = testPoint
        self.obj.httpstatus = httpStatus
        self.obj.sign = signvalue
        self.obj.pretreat = preDict
        self.obj.request = reqestDict
        self.obj.expected = expected
        self.obj.postposition = postposition
        self.obj.updatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.obj.keylist = keyList

        count = self.dbhelper.updateCaseById(self.obj)
        if count > 0:
            QMessageBox.information(self, "提示", "用例修改成功", QMessageBox.Yes, QMessageBox.Yes)
            self.update_case_success_signal.emit()
            self.close()
        else:
            QMessageBox.information(self, "提示", "修改用例失败", QMessageBox.Yes, QMessageBox.Yes)
            # self.clearEdit()

        # def clearEdit(self):
        #     self.caseNameEdit.clear()
        #     self.testPointEdit.clear()
        #     self.faceNameEdit.clear()
        #     self.httpStatusEdit.clear()
        #     self.preTableView.clearContents()
        #     self.reTableView.clearContents()
        #     self.postpositionEdit.setPlainText("")
        #     self.expectedEdit.setPlainText("")


# if __name__ == "__main__":
#     caseModel = Cases()
#     caseModel.caseid = 1
#     caseModel.casename = "dddd"
#     caseModel.testpoint = "dddd"
#     caseModel.pretreat = None
#     caseModel.request = "ddfdf"
#     caseModel.expected = "ddfdf"
#     caseModel.postposition = "ddfdf"
#     caseModel.updatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     caseModel.httpstatus = 200
#     caseModel.sign = "ddfdf"
#     caseModel.faceid = 6
#     caseModel.userid = 38



    # app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    # # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # mainMindow = UpdateCaseDialog(caseModel)
    # mainMindow.show()
    # sys.exit(app.exec_())