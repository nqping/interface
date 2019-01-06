#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/6 13:56
# @Author  : qingping.niu
# @File    : Datetime.py
# @desc    :
import datetime



def getDateTimeNow():
    '''获取当前时间,按年-月-日 时:分:秒 '''
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now_time