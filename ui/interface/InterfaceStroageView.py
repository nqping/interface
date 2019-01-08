#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/6 15:58
# @Author  : qingping.niu
# @File    : InterfaceStroageView.py
# @desc    : 接口管理

import sys,qdarkstyle

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from services.InterfaceManager import InterfaceManager
from ui.interface.CreateInterfaceDialog import CreateInterfaceDialog
from ui.interface.UpdateInterfaceDialog import UpdateInterfaceDialog
from model.Interface import Interface


HEADERS= ['编号','名称','地址','请求类型','数据类型','ContentType','用例数','更新时间','项目','projectId','userId']
class InterfaceStroageView(QWidget):

    def __init__(self):
        super(InterfaceStroageView,self).__init__()
        self.resize(700, 500)

        # 数据表
        self.faceTableView = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecord = 0
        # 每页数据数
        self.pageRecord = 10
        # 记录行数
        self.rowsCount = 0
        # 列数
        self.cloumnCount = len(HEADERS)
        # 数据源
        self.dataSource = []

        self.dbhelper = InterfaceManager()
        self.setUpUI()


    def loadProjectAll(self):
        '''获取所有项目名称和ID'''
        self.dbhelper.getProjectName()


    def setUpUI(self):
        self.layout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()

        font = QFont()
        font.setPixelSize(15)

        rsData = self.dbhelper.getProjectName()

        self.projectBox = QComboBox()
        self.projectBox.addItem("--请选择项目--")

        for data in rsData:
            self.projectBox.addItem(str(data[1]),str(data[0]))

        self.projectBox.setCurrentIndex(0)
        self.projectBox.setObjectName("projectBox")
        self.projectBox.setFixedHeight(32)

        self.searcFaceBtn = QPushButton("查询")
        self.searcFaceBtn.setObjectName("searcFaceBtn")
        self.searcFaceBtn.setFixedHeight(32)
        self.searcFaceBtn.setFont(font)
        self.searcFaceBtn.setIcon(QIcon(QPixmap("./images/search.png")))

        self.addInterfaceBtn = QPushButton("添加")
        self.addInterfaceBtn.setObjectName("addInterfaceBtn")
        self.addInterfaceBtn.setFixedHeight(32)
        self.addInterfaceBtn.setFont(font)

        self.upInterfaceBtn = QPushButton("修改")
        self.upInterfaceBtn.setObjectName("upInterfaceBtn")
        self.upInterfaceBtn.setFixedHeight(32)
        self.upInterfaceBtn.setFont(font)

        self.delInterfaceBtn = QPushButton("删除")
        self.delInterfaceBtn.setObjectName("delInterfaceBtn")
        self.delInterfaceBtn.setFixedHeight(32)
        self.delInterfaceBtn.setFont(font)

        self.Hlayout1.addWidget(self.projectBox)
        self.Hlayout1.addWidget(self.searcFaceBtn)
        self.Hlayout1.addWidget(self.addInterfaceBtn)
        self.Hlayout1.addWidget(self.upInterfaceBtn)
        self.Hlayout1.addWidget(self.delInterfaceBtn)

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

        #创建表格
        self.faceTableView = QTableWidget(self.pageRecord, self.cloumnCount)  # 设置表格显示几行几列
        self.faceTableView.setHorizontalHeaderLabels(HEADERS)  # 设置表头
        self.faceTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置水平方向表格为自适应的伸缩模式
        self.faceTableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格整行选中
        # 将行与列的高度设置为所显示的内容的宽度高度匹配
        self.faceTableView.resizeColumnsToContents()
        self.faceTableView.resizeRowsToContents()
        self.faceTableView.setColumnHidden(0, True)  # 隐藏第一列
        self.faceTableView.setColumnHidden(9,True)
        self.faceTableView.setColumnHidden(10,True)

        self.on_searcFaceBtn_clicked()

        self.layout.addLayout(self.Hlayout1)
        self.layout.addWidget(self.faceTableView)
        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)

        QMetaObject.connectSlotsByName(self)


    def loadInterfaceData(self,id=0,index=0,pageRecord=20):
        datas =self.dbhelper.getInterFaceByCondition(id=id,index=index,pageRecord=pageRecord)
        self.dataSource = []
        self.dataSource = datas
        self.rowCount = len(datas)


    def getPageCount(self,id=0):
        # 总记录数
        self.totalRecord = self.dbhelper.getTotalRecordCount(id)
        # 总页数
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)


    @pyqtSlot()
    def on_searcFaceBtn_clicked(self):
        id = self.projectBox.currentData()
        self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount(id)
        # s = "/" + str(int(self.totalPage)) + "页"
        # self.pageLabel.setText(s)
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)

    # 分页记录查询
    def recordQuery(self, index):
        if self.projectBox.currentData() is None: #查全部数据
            # self.getPageCount()
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            self.loadInterfaceData(index=index,pageRecord=self.pageRecord)
            self.upTableView()
            self.setButtonStatus()
            return
        # 带参数查询并分页
        id = self.projectBox.currentData()
        self.loadInterfaceData(id=id,index=index,pageRecord=self.pageRecord)
        # self.getPageCount()
        if (self.totalRecord == 0):
            QMessageBox.information(self, "提醒", "查询无记录", QMessageBox.Yes, QMessageBox.Yes)
            return
        label = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(label)

        # 重新set 表格
        self.upTableView()
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


    def upTableView(self):
        '''更新表格'''
        self.faceTableView.clearContents()
        for i in range(self.rowCount):
            for j in range(self.cloumnCount):
                temp_data = self.dataSource[i][j]  # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.faceTableView.setItem(i, j, data1)


    def setButtonStatus(self):
        if(self.currentPage==self.totalPage):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(False)
        if(self.currentPage==1):
            self.backButton.setEnabled(True)
            self.prevButton.setEnabled(False)
        if(self.currentPage<self.totalPage and self.currentPage>1):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(True)

    @pyqtSlot()
    def on_addInterfaceBtn_clicked(self):
        createinterfacedialog = CreateInterfaceDialog()
        createinterfacedialog.add_interface_success_signal.connect(self.on_searcFaceBtn_clicked)
        createinterfacedialog.show()
        createinterfacedialog.exec_()

    @pyqtSlot()
    def on_upInterfaceBtn_clicked(self):
        rowNumber = self.faceTableView.currentRow()
        if rowNumber <0:
            QMessageBox.warning(self,"提示","请选中要修改的行")
            return
        value_lst = []
        for i in range(self.cloumnCount):
            if (len(self.faceTableView.item(rowNumber, i).text()) == 0):
                value_lst.append(None)
            else:
                value_lst.append(self.faceTableView.item(rowNumber, i).text())

        updateinterfacedialog = UpdateInterfaceDialog(value_lst)
        updateinterfacedialog.update_interface_success_signal.connect(self.on_searcFaceBtn_clicked)
        updateinterfacedialog.show()
        updateinterfacedialog.exec_()

    @pyqtSlot()
    def on_delInterfaceBtn_clicked(self):
        # 当前行
        rowNumber = self.faceTableView.currentRow()
        if rowNumber <0:
            QMessageBox.information(self,"提示","请选中要删除的行")
            return
        id = self.faceTableView.item(rowNumber, 0).text()

        count = self.dbhelper.deleteByCondition(id)
        if count > 0:
            QMessageBox.information(self,"提示","删除成功")
            self.on_searcFaceBtn_clicked()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = InterfaceStroageView()
    mainMindow.show()
    sys.exit(app.exec_())



