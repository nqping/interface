#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/2 14:05
# @Author  : qingping.niu
# @File    : SignInBiz.py
# @desc    : 登录业务

from db.DBManager import DBManager


class SignInBiz(object):

    def __init__(self):
        self.dbhelper = DBManager()

    def checkUser(self,userName,passWord):
        sql = 'select user_id,user_name,password from tc_user where user_name=%s and password=%s'
        dict = self.dbhelper.executeQuery_one(sql,(userName,passWord))
        if dict != {}:
            return dict['user_id']
        return 0
