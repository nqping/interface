#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 16:57
# @Author  : qingping.niu
# @File    : CaseStroageView.py
# @desc    : 用例列表页

import sys,qdarkstyle,datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from services.CaseManager import CaseManager
from services.InterfaceManager import InterfaceManager
from ui.case.CreateCaseDialog import CreateCaseDialog
from ui.case.UpdateCaseDialog import UpdateCaseDialog
from model.Cases import Cases
from utils.globalvar import GlobalVar as gl

HEADERS= ['编号','用例名称','测试点','前置处理','请求参数','期望结果','后置处理','编辑时间','请求状态','签名','faceId','userId','keyList']

class CaseStroageView(QWidget):

    def __init__(self):
        super(CaseStroageView,self).__init__()
        self.userid = gl.get_value("userId")
        self.resize(700, 500)
        # 数据表
        self.tableView = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecord = 0
        # 每页数据数
        self.pageRecord = 10

        self.rowsCount = 0  # 行数
        self.cloumnCount = len(HEADERS)  # 列数

        # 数据源
        self.dataSource = []

        self.dbhelper = CaseManager()
        self.faceManager = InterfaceManager()
        self.setUpUI()

    def setUpUI(self):
        self.layout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()

        font = QFont()
        font.setPixelSize(15)


        proDatas = self.faceManager.getProjectName()

        self.projectBox = QComboBox()
        self.projectBox.setObjectName("projectBox")
        self.projectBox.addItem("--项目--")

        for data in proDatas:
            self.projectBox.addItem(str(data[1]), str(data[0]))


        self.interfaceBox = QComboBox()
        self.interfaceBox.addItem("--接口--")
        self.interfaceBox.setCurrentIndex(0)
        self.interfaceBox.setObjectName("interfaceBox")
        self.interfaceBox.setFixedHeight(32)

        self.searcBtn = QPushButton("查询")
        self.searcBtn.setObjectName("searcBtn")
        self.searcBtn.setFixedHeight(32)
        self.searcBtn.setFont(font)
        self.searcBtn.setIcon(QIcon(QPixmap("./images/search.png")))

        self.addBtn = QPushButton("添加")
        self.addBtn.setObjectName("addBtn")
        self.addBtn.setFixedHeight(32)
        self.addBtn.setFont(font)

        self.updateBtn = QPushButton("修改")
        self.updateBtn.setObjectName("updateBtn")
        self.updateBtn.setFixedHeight(32)
        self.updateBtn.setFont(font)

        self.runBtn = QPushButton("运行")
        self.runBtn.setObjectName("runBtn")
        self.runBtn.setFixedHeight(32)
        self.runBtn.setFont(font)

        self.deleteBtn = QPushButton("删除")
        self.deleteBtn.setObjectName("deleteBtn")
        self.deleteBtn.setFixedHeight(32)
        self.deleteBtn.setFont(font)

        self.Hlayout1.addWidget(self.projectBox)
        self.Hlayout1.addWidget(self.interfaceBox)
        self.Hlayout1.addWidget(self.searcBtn)
        self.Hlayout1.addWidget(self.addBtn)
        self.Hlayout1.addWidget(self.updateBtn)
        self.Hlayout1.addWidget(self.runBtn)
        self.Hlayout1.addWidget(self.deleteBtn)

        # Hlayout2初始化
        self.jumpToLabel = QLabel("跳转到第")
        self.jumpToLabel.setFixedWidth(60)
        self.pageEdit = QLineEdit()
        self.pageEdit.setFixedWidth(30)
        s = "/" + str(self.totalPage) + "页"
        self.pageLabel = QLabel(s)
        self.jumpToButton = QPushButton("跳转")
        self.jumpToButton.setObjectName("jumpToButton")
        self.prevButton = QPushButton("上一页")
        self.prevButton.setObjectName("prevButton")
        self.prevButton.setFixedWidth(60)
        self.backButton = QPushButton("下一页")
        self.backButton.setObjectName("backButton")
        self.backButton.setFixedWidth(60)

        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.jumpToLabel)
        Hlayout.addWidget(self.pageEdit)
        Hlayout.addWidget(self.pageLabel)
        Hlayout.addWidget(self.jumpToButton)
        Hlayout.addWidget(self.prevButton)
        Hlayout.addWidget(self.backButton)
        widget = QWidget()
        widget.setLayout(Hlayout)
        widget.setFixedWidth(350)
        self.Hlayout2.addWidget(widget)

        # 创建表格
        self.tableView = QTableWidget(self.pageRecord, self.cloumnCount)  # 设置表格显示几行几列
        self.tableView.setHorizontalHeaderLabels(HEADERS)  # 设置表头
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置水平方向表格为自适应的伸缩模式
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格整行选中
        # 将行与列的高度设置为所显示的内容的宽度高度匹配
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.setFocusPolicy(Qt.NoFocus)#去掉选中单元格时的虚线框
        self.tableView.setColumnHidden(8, True)# 隐藏第一列
        self.tableView.setColumnHidden(9, True)
        self.tableView.setColumnHidden(10, True)
        self.tableView.setColumnHidden(11, True)
        self.tableView.setColumnHidden(12, True)

        self.on_searcBtn_clicked()
        self.layout.addLayout(self.Hlayout1)
        self.layout.addWidget(self.tableView)
        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)

        QMetaObject.connectSlotsByName(self)

    def loadCaseList(self,id=None,index=0,pageRecord=20):
        datas = self.dbhelper.getCaseByCondition(face_id=id,index=index,pageRecord=pageRecord)
        self.dataSource = datas
        self.rowCount = len(datas)

    def getPageCount(self,id=None):
        # 总记录数
        self.totalRecord = self.dbhelper.getTotalRecordCount(face_id=id)
        # 总页数
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)

    @pyqtSlot(str)
    def on_projectBox_currentTextChanged(self,value):
        proId = self.projectBox.currentData()
        if proId is not None:
            rsData = self.faceManager.getFaceListByProId(proId)
            for data in rsData:
                self.interfaceBox.addItem(str(data[1]),str(data[0]))
            self.interfaceBox.setCurrentIndex(1)

    @pyqtSlot()
    def on_searcBtn_clicked(self):
        faceId = self.interfaceBox.currentData() #获取数据
        self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount(id=faceId)
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)

    # 分页记录查询
    def recordQuery(self, index):
        faceId = self.interfaceBox.currentData()
        if faceId is None:
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            self.loadCaseList(index=index,pageRecord=self.pageRecord)
            self.upTableView()  # 更新表格
            self.setButtonStatus()
            return

        #带参数查询
        self.loadCaseList(id=faceId,index=index, pageRecord=self.pageRecord)
        if (self.totalRecord == 0):
            QMessageBox.information(self, "提醒", "查询无记录", QMessageBox.Yes, QMessageBox.Yes)
            return
        label = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(label)
        self.upTableView()  # 更新表格
        self.setButtonStatus()


    @pyqtSlot()
    def on_jumpToButton_clicked(self):
        '''跳转'''
        if (self.pageEdit.text().isdigit()):
            self.currentPage = int(self.pageEdit.text())
            if (self.currentPage > self.totalPage):
                self.currentPage = self.totalPage
            if (self.currentPage <= 1):
                self.currentPage = 1
        else:
            self.currentPage = 1
        index = (self.currentPage - 1) * self.pageRecord
        self.pageEdit.setText(str(self.currentPage))
        self.recordQuery(index)

    @pyqtSlot()
    def on_prevButton_clicked(self):
        self.currentPage -= 1
        if (self.currentPage <= 1):
            self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)

    @pyqtSlot()
    def on_backButton_clicked(self):
        '''下一页'''
        self.currentPage += 1
        if (self.currentPage >= int(self.totalPage)):
            self.currentPage = int(self.totalPage)
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)

    @pyqtSlot()
    def on_addBtn_clicked(self):

        face_id = self.interfaceBox.currentData()
        if face_id is None:
            QMessageBox.warning(self,"提示","请选择接口")
        else:
            facename = self.interfaceBox.currentText()
            createcasedialog = CreateCaseDialog(faceid=face_id,facename=facename,userid=self.userid)
            createcasedialog.add_case_success_signal.connect(self.on_searcBtn_clicked)
            createcasedialog.show()
            createcasedialog.exec_()

    @pyqtSlot()
    def on_updateBtn_clicked(self):
        row = self.tableView.currentRow()
        if row < 0 :
            QMessageBox.warning(self, "提示", "请选中要修改的行")
            return
        value_lst = []
        for i in range(self.cloumnCount):
            if (len(self.tableView.item(row, i).text()) == 0):
                value_lst.append("")
            else:
                value_lst.append(self.tableView.item(row, i).text())


        caseModel = Cases()
        caseModel.caseid = value_lst[0]
        caseModel.casename = value_lst[1]
        caseModel.testpoint = value_lst[2]
        caseModel.pretreat = value_lst[3]
        caseModel.request = value_lst[4]
        caseModel.expected = value_lst[5]
        caseModel.postposition = value_lst[6]
        caseModel.updatetime =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        caseModel.httpstatus = value_lst[8]
        caseModel.sign = value_lst[9]
        caseModel.faceid = value_lst[10]
        caseModel.userid = value_lst[11]
        caseModel.keylist = value_lst[12]

        updatecasedialog = UpdateCaseDialog(caseModel)
        updatecasedialog.update_case_success_signal.connect(self.on_searcBtn_clicked)
        updatecasedialog.show()
        updatecasedialog.exec_()


    @pyqtSlot()
    def on_deleteBtn_clicked(self):
        # 是否删除的对话框
        reply = QMessageBox.question(self, '消息', '确定删除?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            row = self.tableView.currentRow()
            caseid = self.tableView.item(row,0).text()
            count = self.dbhelper.deleteCaseById(caseid)
            if count > 0:
                self.tableView.removeRow(row)
            else:
                QMessageBox.information(self,"消息","用例删除失败")


    @pyqtSlot()
    def on_runBtn_clicked(self):
        row = self.tableView.currentRow()
        if row < 0:
            QMessageBox.warning(self, "提示", "请选中要执行的用例")
            return
        #获取case数据
        value_lst = []
        for i in range(self.cloumnCount):
            if (len(self.tableView.item(row, i).text()) == 0):
                value_lst.append(None)
            else:
                value_lst.append(self.tableView.item(row, i).text())
        caseModel = Cases()
        caseModel.caseid = value_lst[0]
        caseModel.casename = value_lst[1]
        caseModel.testpoint = value_lst[2]
        caseModel.pretreat = value_lst[3]
        caseModel.request = value_lst[4]
        caseModel.expected = value_lst[5]
        caseModel.postposition = value_lst[6]
        caseModel.updatetime = value_lst[7]
        caseModel.httpstatus = value_lst[8]
        caseModel.sign = value_lst[9]
        caseModel.faceid = value_lst[10]
        caseModel.userid = value_lst[11]
        caseModel.keylist = value_lst[12]

        self.dbhelper.runCase(caseModel)


    def upTableView(self):
        '''更新表格'''
        self.tableView.clearContents()
        for i in range(self.rowCount):
            for j in range(self.cloumnCount):
                temp_data = self.dataSource[i][j]  # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                #data1.setCheckState(Qt.Unchecked) #设置复选框,未选中状态
                self.tableView.setItem(i, j, data1)


    def setButtonStatus(self):
        if (self.currentPage == self.totalPage):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(False)
        if (self.currentPage == 1):
            self.backButton.setEnabled(True)
            self.prevButton.setEnabled(False)
        if (self.currentPage < self.totalPage and self.currentPage > 1):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = CaseStroageView()
    mainMindow.show()
    sys.exit(app.exec_())



