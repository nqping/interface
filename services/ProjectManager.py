#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/3 14:51
# @Author  : qingping.niu
# @File    : ProjectManager.py
# @desc    :

import datetime
from db.DBManager import DBManager
from model.Project import Project


class ProjectManager(object):
    def __init__(self):
        self.mydb = DBManager()

    def getObjectAll(self):
        sql="select * from tc_project"
        dict = self.mydb.executeQuery_all(sql)
        return dict

    def getTotalRecordCount(self,projectName=None):
        '''获取总记录数'''
        sqlBuilder = []
        sqlBuilder.append("select * from tc_project where 1=1")
        if projectName is not None:
            sqlBuilder.append(" and pro_name like '%s'" %('%'+projectName+'%') )
        recordCount = self.mydb.executeQuery_count(sql=''.join(sqlBuilder))
        return recordCount

    def getObjectByCondition(self,projectName=None,index=0,pageRecord=10):
        '''带条件查询'''
        sqlBuilder = []
        sqlBuilder.append("select * from tc_project where 1=1")
        if projectName is not None:
            sqlBuilder.append(" and pro_name like '%s'" %('%'+projectName+'%'))

        sqlBuilder.append(" order by update_time desc limit %d,%d" %(index,pageRecord))
        # print(''.join(sqlBuilder))
        rsData = self.mydb.executeQuery_all(sql=''.join(sqlBuilder))
        if rsData:
            return rsData
        return ()

    def createProject(self,projectName=None,remark=None,creator=None):
        '''创建项目'''
        sql="insert into tc_project (pro_name,update_time,creator,remark) values(%s,%s,%s,%s)"
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = (projectName,now_time,creator,remark)
        count = self.mydb.insert_params(sql,params)
        return count

    def deleteByCondition(self,projectId=0):
        sql="delete from tc_project where pro_id=%s"
        count = self.mydb.delete_params(sql,(projectId))
        return count


    def updateByCondition(self,projectId=0,projectName=None,remark=None,creator=None):
        sql="update tc_project set pro_name=%s,remark=%s,update_time=%s,creator=%s where pro_id=%s"
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params=(projectName,remark,now_time,creator,projectId)
        count = self.mydb.update_params(sql,params)
        return count




if __name__=='__main__':
    p = ProjectManager()
    # count = p.getTotalRecordCount()
    # print(count)
    # rsdata = p.getObjectByCondition("Joy",0,10)
    # print(rsdata)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    count = p.createProject("ssss","dfdfdfd","niuqingping")
    print(count)
