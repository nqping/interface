#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/3 14:38
# @Author  : qingping.niu
# @File    : ProjectStroageView.py
# @desc    : 项目管理

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from services.ProjectManager import ProjectManager
import sys,qdarkstyle
from utils.globalvar import GlobalVar as gl
from ui.project.CreateProjectDialog import CreateProjectDialog
from ui.project.UpdateProjectDialog import UpdateProjectDialog

HEADERS= ['编号','名称','创建时间','创建者','备注']

class ProjectStroageView(QWidget,QAbstractTableModel):
    def __init__(self):
        super(ProjectStroageView,self).__init__()
        self.resize(700, 500)
        # 查询模型
        self.queryModel = None
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

        self.rowsCount = 0 #行数
        self.cloumnCount =len(HEADERS) #列数

        self.dbhelper = ProjectManager()
        self.proDatas = [] #数据源
        # self.loadProjectData()  # 获取数据
        print(gl.get_value("userName"))
        self.setUpUI()


    def loadProjectData(self,projectName=None,index=0,pageRecord=10):
        '''加载数据'''
        proData = self.dbhelper.getObjectByCondition(projectName=projectName,index=index,pageRecord=pageRecord)
        self.proDatas = []
        self.rowCount = len(proData)
        self.proDatas = proData


    def setUpUI(self):
        self.layout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()

        font = QFont()
        font.setPixelSize(15)

        # Hlayout1控件的初始化
        self.searchEdit = QLineEdit()
        self.searchEdit.setFixedHeight(32)

        self.searchEdit.setPlaceholderText("输入项目名称")
        self.searchEdit.setFont(font)

        self.searchButton = QPushButton("查询")
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setFixedHeight(32)
        self.searchButton.setFont(font)
        self.searchButton.setIcon(QIcon(QPixmap("./images/search.png")))

        self.addProjectBtn = QPushButton("添加")
        self.addProjectBtn.setObjectName("addProjectBtn")
        self.addProjectBtn.setFixedHeight(32)
        self.addProjectBtn.setFont(font)

        self.updateBtn = QPushButton("修改")
        self.updateBtn.setObjectName("updateBtn")
        self.updateBtn.setFixedHeight(32)
        self.updateBtn.setFont(font)


        self.deleteBtn = QPushButton("删除")
        self.deleteBtn.setObjectName("deleteBtn")
        self.deleteBtn.setFixedHeight(32)
        self.deleteBtn.setFont(font)


        self.Hlayout1.addWidget(self.searchEdit)
        self.Hlayout1.addWidget(self.searchButton)
        self.Hlayout1.addWidget(self.addProjectBtn)
        self.Hlayout1.addWidget(self.updateBtn)
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


        self.tableView = QTableWidget(self.pageRecord, self.cloumnCount) #设置表格显示几行几列
        self.tableView.setHorizontalHeaderLabels(HEADERS) #设置表头
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置水平方向表格为自适应的伸缩模式
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows) #设置表格整行选中
        #将行与列的高度设置为所显示的内容的宽度高度匹配
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.setColumnHidden(0,True) #隐藏第一列

        self.on_searchButton_clicked()
        self.layout.addLayout(self.Hlayout1)
        self.layout.addWidget(self.tableView)
        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)



        QMetaObject.connectSlotsByName(self)

    # # 得到总记录数
    # def getTotalRecordCount(self):
    #     self.totalRecord = self.dbhelper.getTotalRecordCount()
    #     return

    # 得到总页数和总记录数
    def getPageCount(self,projectName=None):
        #总记录数
        self.totalRecord = self.dbhelper.getTotalRecordCount(projectName=projectName)
        # 总页数
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        return

    def upTableView(self):
        '''更新表格'''
        self.tableView.clearContents()
        for i in range(self.rowCount):
            for j in range(self.cloumnCount):
                temp_data = self.proDatas[i][j]  # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.tableView.setItem(i, j, data1)

    # 分页记录查询
    def recordQuery(self,index):
        if (self.searchEdit.text() == ""):  # 查全部数据并分页显示
            self.getPageCount()
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            self.loadProjectData(index=index,pageRecord=self.pageRecord)  #加载数据
            self.upTableView()  # 更新表格
            self.setButtonStatus()
            return
        #带参数查询并分页
        temp = self.searchEdit.text()
        self.loadProjectData(projectName=temp, index=index, pageRecord=self.pageRecord)  # 按条件查数据
        self.getPageCount(projectName=temp)
        if (self.totalRecord == 0):
            QMessageBox.information(self, "提醒", "查询无记录", QMessageBox.Yes, QMessageBox.Yes)
            return
        label = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(label)

        # 重新set 表格
        self.upTableView()
        self.setButtonStatus()


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
    def on_searchButton_clicked(self):
        temp = self.searchEdit.text()
        self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount(projectName=temp)
        s = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(s)
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)

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
    def on_addProjectBtn_clicked(self):
        createprojectdialog = CreateProjectDialog()
        createprojectdialog.add_project_success_signal.connect(self.on_searchButton_clicked)
        createprojectdialog.show()
        createprojectdialog.exec_()


    @pyqtSlot()
    def on_updateBtn_clicked(self):
        rowNumber = self.tableView.currentRow()
        if rowNumber <0:
            QMessageBox.information(self,"提示","请选中要修改的行")
            return
        value_lst = []
        for i in range(self.cloumnCount):
            if (len(self.tableView.item(rowNumber, i).text()) == 0):
                value_lst.append(None)
            else:
                value_lst.append(self.tableView.item(rowNumber, i).text())

        updateprojectdialog = UpdateProjectDialog(projectId=value_lst[0],projectName=value_lst[1],userName=value_lst[3],remark=value_lst[4])
        updateprojectdialog.update_project_success_signal.connect(self.on_searchButton_clicked)
        updateprojectdialog.show()
        updateprojectdialog.exec_()

        # self.dbhelper.updateByCondition()


        # rowNumber = self.tableView.rowCount()
        # if rowNumber:
        #     QMessageBox.information(self,"提示","请选中行")
        #     return
        # value_lst = []
        # for i in range(self.cloumnCount):
        #     if (len(self.tableView.item(rowNumber - 1, i).text()) == 0):
        #         value_lst.append(None)
        #     else:
        #         value_lst.append(self.tableView.item(rowNumber - 1, i).text())
        # tup_va_lst = []
        # for cl, va in zip(self.cloumnCount, value_lst):
        #     tup_va_lst.append((cl, va))





    @pyqtSlot()
    def on_deleteBtn_clicked(self):
        # 当前行
        rowNumber = self.tableView.currentRow()
        if rowNumber <0:
            QMessageBox.information(self,"提示","请选中要删除的行")
            return
        id = self.tableView.item(rowNumber, 0).text()

        count = self.dbhelper.deleteByCondition(id)
        if count > 0:
            QMessageBox.information(self,"提示","删除成功")
            self.on_searchButton_clicked()











if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = ProjectStroageView()
    mainMindow.show()
    sys.exit(app.exec_())