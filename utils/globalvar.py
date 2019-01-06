#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 17:46
# @Author  : qingping.niu
# @File    : globalvar.py
# @desc    : 全局变量管理
import json

from .log import LOG

class GlobalVar(object):
    global_dict = {}

    def set_value(name, value):
        GlobalVar.global_dict[name] = value

    def get_value(name, defValue=None):
        try:
            return GlobalVar.global_dict[name]
        except KeyError:
            return defValue


