#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/12 13:21
# @Author  : qingping.niu
# @File    : log.py
# @desc    : 日志记录打印

import os,time,sys
from functools import wraps   #装饰器
import logbook
from logbook import Logger,StreamHandler,FileHandler,TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler  #日志打印到屏幕


def log_type(record,handler):
    log = "[{date}] [{level}] [{filename}] [{func_name}] [{lineno}] {msg}".format(
        date = record.time,                              # 日志时间
        level = record.level_name,                       # 日志等级
        filename = os.path.split(record.filename)[-1],   # 文件名
        func_name = record.func_name,                    # 函数名
        lineno = record.lineno,                          # 行号
        msg = record.message                             # 日志内容
    )
    return log

#日志存放路径
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
today = time.strftime('%Y%m%d', time.localtime(time.time()))
full_path = os.path.join(log_dir, today)
if not os.path.exists(full_path):
    os.makedirs(full_path)


def get_logger(logname):
    user_log = logbook.Logger('log')

    logbook.set_datetime_format("local")  # 格式化时间

    # 日志打印到屏幕
    log_std = ColorizedStderrHandler(bubble=True)
    log_std.formatter = log_type

    # 日志打印到文件
    log_file = TimedRotatingFileHandler(os.path.join(full_path, '%s.log' % logname),
                                        date_format='%Y-%m-%d', bubble=True,
                                        encoding='utf-8')  # 日期分割显示文件(带日期的)
    log_file.formatter = log_type

    user_log.handlers = []
    user_log.handlers.append(log_file)
    user_log.handlers.append(log_std)

    return user_log


LOG = get_logger("log")

#可不写参数
def logger(func):
    """ logger wrapper """
    @wraps(func)
    def log(*args,**kwargs):
        try:
            LOG.info("当前运行方法,{}".format(func.__name__))
            LOG.info("全部args参数参数信息 , {}".format(str(args)))
            LOG.info("全部kwargs参数信息 , {}".format(str(kwargs)))
            return func(*args,**kwargs)
        except Exception as e:
            get_logger().error("{func.__name__} is error,here are details:{traceback.format_exc()}",e)
    return log


#描述类的
def desclog(param):
    """ fcuntion from logger meta """
    def wrap(function):
        """ logger wrapper """
        @wraps(function)
        def _wrap(*args, **kwargs):
            """ wrap tool """
            LOG.info("当前模块 {}".format(param))
            LOG.info("全部args参数参数信息 , {}".format(str(args)))
            LOG.info("全部kwargs参数信息 , {}".format(str(kwargs)))
            return function(*args, **kwargs)
        return _wrap
    return wrap
