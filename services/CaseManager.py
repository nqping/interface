#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/6 16:18
# @Author  : qingping.niu
# @File    : CaseManager.py
# @desc    :

from db.DBManager import DBManager

class CaseManager(object):
    def __init__(self):
        self.mydb = DBManager()