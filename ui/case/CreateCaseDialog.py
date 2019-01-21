#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 16:57
# @Author  : qingping.niu
# @File    : CreateCaseDialog.py
# @desc    :

import sys,qdarkstyle,sip,datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTextEdit
from services.CaseManager import CaseManager
from model.Cases import Cases
from utils.md5Utils import md5Encode
from utils.log import LOG


keyList=[]
class CreateCaseDialog(QDialog):
    add_case_success_signal = pyqtSignal()
    # delete_widget = pyqtSignal(str)

    def __init__(self,faceid=None,facename=None,userid=None):
        super(CreateCaseDialog,self).__init__()
        self.casedb = CaseManager()

        self.faceid = faceid
        self.facename = facename
        self.userid = userid

        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)  # 设置弹框出现后,父窗口不可活动
        self.setWindowTitle("新增用例")

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
        faceNameLabel = QLabel("接口:")
        # userNameLabel = QLabel("创建者:")
        
        caseNameLabel.setFont(font)
        testPointLabel.setFont(font)
        httpStatusLabel.setFont(font)
        faceNameLabel.setFont(font)
        # userNameLabel.setFont(font)
        
        self.caseNameEdit = QLineEdit()
        self.caseNameEdit.setObjectName("caseNameEdit")
        self.caseNameEdit.setPlaceholderText("输入测试名称")
        self.caseNameEdit.setFixedHeight(30)
        self.caseNameEdit.setFont(font)

        self.testPointEdit = QLineEdit()
        self.testPointEdit.setObjectName("testPointEdit")
        self.testPointEdit.setPlaceholderText("输入测试点")
        self.testPointEdit.setFixedHeight(30)
        self.testPointEdit.setFont(font)

        self.httpStatusEdit = QLineEdit()
        self.httpStatusEdit.setObjectName("httpStatusEdit")
        self.httpStatusEdit.setPlaceholderText("http请求状态:200")
        self.httpStatusEdit.setFixedHeight(35)
        self.httpStatusEdit.setFont(font)

        self.faceNameEdit = QLineEdit()
        self.faceNameEdit.setText(self.facename)
        self.faceNameEdit.setObjectName("faceNameEdit")
        self.faceNameEdit.setPlaceholderText("接口名称")
        self.faceNameEdit.setFixedHeight(30)
        self.faceNameEdit.setFont(font)
        self.faceNameEdit.setReadOnly(True)

        # self.userNameEdit = QLineEdit()
        # self.userNameEdit.setObjectName("userNameEdit")
        # self.userNameEdit.setPlaceholderText("")
        # self.userNameEdit.setFixedHeight(30)
        # self.userNameEdit.setFont(font)


        font.setPixelSize(16)
        # button控件
        self.submitBtn = QPushButton("提交")
        self.submitBtn.setObjectName("submitBtn")
        self.submitBtn.setFont(font)
        self.submitBtn.setFixedHeight(32)
        self.submitBtn.setFixedWidth(140)

        self.clearBtn = QPushButton("重置")
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.setFont(font)
        self.clearBtn.setFixedHeight(32)
        self.clearBtn.setFixedWidth(140)

        self.formlayout.addRow(caseNameLabel,self.caseNameEdit)
        self.formlayout.addRow(testPointLabel,self.testPointEdit)
        self.formlayout.addRow(httpStatusLabel,self.httpStatusEdit)
        # self.formlayout.addRow(userNameLabel,self.userNameEdit)
        self.formlayout.addRow(faceNameLabel,self.faceNameEdit)

        font.setPixelSize(14)
        self.tabwidget = QTabWidget()
        self.tabwidget.setFont(font)
        self.tab_pretreat_params() #前置处理
        self.tab_request_params() #请求参数
        self.tab_expected_params() #预期结果
        self.tab_postposition_params() #后置处理

        self.vboxlayout.addWidget(self.tabwidget)

        myHbox = QHBoxLayout()
        myHbox.addWidget(self.submitBtn)
        myHbox.addWidget(self.clearBtn)

        self.mainHboxLayout.addLayout(self.formlayout)
        self.mainHboxLayout.addLayout(self.vboxlayout)
        self.mainHboxLayout.addLayout(myHbox)

        QMetaObject.connectSlotsByName(self)

    def tab_pretreat_params(self):
        formlayout = QFormLayout()
        vboxlayout = QVBoxLayout()

        addRowBtn = QPushButton()
        addRowBtn.setIcon(QIcon("../images/112.png"))
        addRowBtn.setFixedHeight(30)
        addRowBtn.setFixedWidth(30)

        addRowBtn.clicked.connect(self.insertRow_pretreat)

        self.preTableView = QTableWidget(0, 3)
        self.preTableView.setHorizontalHeaderLabels([ "参数名", "值","操作"])
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
        formlayout1 = QFormLayout()
        vboxlayout1 = QVBoxLayout()

        self.reTableView = QTableWidget(0,4)
        self.reTableView.setHorizontalHeaderLabels(["是否签名","参数名","值","操作"])
        self.reTableView.setShowGrid(True)
        self.reTableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格整行选中

        addRowBtn = QPushButton()
        addRowBtn.setIcon(QIcon("../../images/112.png"))
        addRowBtn.setFixedHeight(30)
        addRowBtn.setFixedWidth(30)
        addRowBtn.clicked.connect(self.insertRow_request)

        self.signLabel = QLabel("")

        self.reTableView.horizontalHeader().resizeSection(0, 80) #重置列宽
        self.reTableView.horizontalHeader().resizeSection(1, 150)
        self.reTableView.horizontalHeader().resizeSection(2, 250)
        self.reTableView.horizontalHeader().resizeSection(3, 50)

        formlayout1.addRow(addRowBtn,self.signLabel)
        vboxlayout1.addLayout(formlayout1)
        vboxlayout1.addWidget(self.reTableView)

        widget = QWidget()
        widget.setLayout(vboxlayout1)
        self.tabwidget.addTab(widget,"请求参数")


    def tab_expected_params(self):
        vboxlayout1 = QVBoxLayout()

        font = QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)

        self.expectedEdit = QTextEdit()
        vboxlayout1.addWidget(self.expectedEdit)
        widget = QWidget()
        widget.setLayout(vboxlayout1)
        self.tabwidget.addTab(widget, "预期结果")


    def tab_postposition_params(self):
        vboxlayout1 = QVBoxLayout()

        self.postpositionEdit = QTextEdit()
        vboxlayout1.addWidget(self.postpositionEdit)
        widget = QWidget()
        widget.setLayout(vboxlayout1)
        self.tabwidget.addTab(widget, "后置处理")


    def insertRow_request(self):
        '''添加行(请求参数)'''
        row = self.reTableView.rowCount()# 获取行数
        self.reTableView.insertRow(row)# 在末尾插入一空行

        checkbox = QCheckBox()
        checkbox.stateChanged.connect(lambda :self.checkboxState(checkbox))

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


    def deleteRow_request(self):
        '''删除行(请求参数)'''
        row = self.reTableView.currentRow() #获取当前行
        del_d =self.reTableView.cellWidget(row,1).text()
        print(del_d)

        self.reTableView.removeRow(row)# 删除行



    def deleteRow_pretreat(self):
        '''删除行(前置参数)'''
        row = self.preTableView.currentRow()
        # ss = self.preTableView.cellWidget(row,1).text()
        self.preTableView.removeRow(row)

    def insertRow_pretreat(self):
        '''插入行(前置参数)'''
        row = self.preTableView.rowCount()# 获取行数
        self.preTableView.insertRow(row)# 在末尾插入一空行

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

    def checkboxState(self,checkbox):
        row = self.reTableView.currentRow()
        if checkbox.isChecked():
            signkey = self.reTableView.cellWidget(row,1).text()
            keyList.append(signkey)
            self.signLabel.setText("签名顺序:"+str(keyList))
        else:
            signkey = self.reTableView.cellWidget(row, 1).text()
            if signkey in keyList:
                keyList.remove(signkey)

            self.signLabel.setText("签名顺序:" + str(keyList))

    @pyqtSlot()
    def on_submitBtn_clicked(self):
        caseName = self.caseNameEdit.text()
        testPoint = self.testPointEdit.text()
        httpStatus = self.httpStatusEdit.text()
        #前置处理
        preDict = {}
        rowCount = self.preTableView.rowCount()
        for i in range(rowCount):
            key = self.preTableView.cellWidget(i,0).text()
            value = self.preTableView.cellWidget(i,1).text()
            preDict.setdefault(key,value)

        #请求参数
        reqestDict = {}
        rowCount = self.reTableView.rowCount()
        for i in range(rowCount):
            key = self.reTableView.cellWidget(i,1).text()
            value = self.reTableView.cellWidget(i,2).text()
            reqestDict.setdefault(key,value)

        #预期结果
        expected = self.expectedEdit.toPlainText()
        #后置处理
        postposition = self.postpositionEdit.toPlainText()

        #获取签名
        temp = []
        signvalue=""
        if len(keyList)>0:
            for mykey in keyList:
                val = reqestDict.get(mykey)
                temp.append(val)
            signvalue = md5Encode(temp)
            reqestDict.setdefault("sign", signvalue)

        LOG.info('签名:%s,%s' % (keyList, signvalue))

        caseObj = Cases()
        caseObj.casename = caseName
        caseObj.faceid = self.faceid
        caseObj.userid = self.userid
        caseObj.testpoint = testPoint
        caseObj.httpstatus = httpStatus
        caseObj.sign = signvalue
        caseObj.pretreat = preDict
        caseObj.request = reqestDict
        caseObj.expected = expected
        caseObj.postposition = postposition
        caseObj.updatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        caseObj.keylist = keyList

        count = self.casedb.createCase(caseObj)
        if count > 0:
            QMessageBox.information(self, "提示", "用例添加成功", QMessageBox.Yes, QMessageBox.Yes)
            self.add_case_success_signal.emit()
            self.close()
            self.clearEdit()

    def clearEdit(self):
        self.caseNameEdit.clear()
        self.testPointEdit.clear()
        self.faceNameEdit.clear()
        self.httpStatusEdit.clear()
        self.preTableView.clearContents()
        self.reTableView.clearContents()
        self.postpositionEdit.setPlainText("")
        self.expectedEdit.setPlainText("")









if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = CreateCaseDialog()
    mainMindow.show()
    sys.exit(app.exec_())





