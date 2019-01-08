#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/6 16:18
# @Author  : qingping.niu
# @File    : InterfaceManager.py
# @desc    :

from db.DBManager import DBManager
from utils.log import LOG
# from model.Interface import Interface

class InterfaceManager(object):
    def __init__(self):
        self.mydb = DBManager()


    def getTotalRecordCount(self,id=None):
        '''获取总记录数'''
        sqlBuilder = []
        sqlBuilder.append("select * from tc_interface where 1=1")
        if id is not None:
            sqlBuilder.append(" and projectId=%s"%id)
        recordCount = self.mydb.executeQuery_count(''.join(sqlBuilder))
        LOG.info(''.join(sqlBuilder))
        return recordCount

    def getProjectName(self):
        '''获取项目名称和id'''
        sql="select pro_id,pro_name from tc_project"
        rsData = self.mydb.executeQuery_all(sql)
        return rsData

    def getInterFaceByCondition(self,id=-1,index=0,pageRecord=20):
        '''根据条件查询接口信息,并分页'''
        sqlBuilder = []
        sqlBuilder.append("select id,faceName,address,requestType,dataType,contentType,caseCount,createTime,projectName,projectId,userId from tc_interface where 1=1")
        if id != 0:
            sqlBuilder.append(" and projectId=%d" % int(id))
        sqlBuilder.append(" order by createTime desc limit %d,%d" %(index,pageRecord))
        rsData = self.mydb.executeQuery_all(''.join(sqlBuilder))
        LOG.info(''.join(sqlBuilder))
        return  rsData

    def addInterface(self,Interface=None):
        '''插入数据'''
        sqlBuilder = []
        sqlBuilder.append("insert into tc_interface (faceName,address,requestType,dataType,contentType,createTime,projectName,projectId,userId)")
        sqlBuilder.append(" values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        params = (Interface.faceName,Interface.address,Interface.requestType,Interface.dataType,Interface.contentType,Interface.createTime,Interface.projectName,Interface.projectId,Interface.userId)
        LOG.info(''.join(sqlBuilder))
        count = self.mydb.insert_params(sql = ''.join(sqlBuilder),params=params)
        return count

    def updateInterface(self,Interface=None):
        '''修改数据'''
        sqlBuilder = []
        sqlBuilder.append("update tc_interface set faceName=%s,address=%s,requestType=%s,dataType=%s,contentType=%s,createTime=%s,caseCount=%s,projectName=%s,projectId=%s,userId=%s")
        sqlBuilder.append(" where id=%s")
        params =(Interface.faceName,Interface.address,Interface.requestType,Interface.dataType,Interface.contentType,Interface.createTime,Interface.caseCount,Interface.projectName,Interface.projectId,Interface.userId,Interface.faceId)
        LOG.info(''.join(sqlBuilder))
        LOG.info(params)
        count = self.mydb.update_params(sql=''.join(sqlBuilder),params=params)
        return count

    def deleteByCondition(self,id):
        '''删除数据'''
        sql="delete from tc_interface where id=%s"
        count = self.mydb.delete_params(sql,(id))
        return count


if __name__=='__main__':
    mydb = InterfaceManager()
    dd = mydb.getTotalRecordCount(6)
    print(dd)
    # mydb.getProjectName()




