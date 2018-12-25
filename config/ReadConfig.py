#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 10:08
# @Author  : qingping.niu
# @File    : ReadConfig.py
# @desc    : 读取配置文件


import configparser
import os

proDir = os.path.split(os.path.realpath(__file__))[0]
#将path分割成路径名和文件名
configPath = os.path.join(proDir, "configure.conf")
#将多个路径组合后返回

"""获取数据库配置文件"""
def getConfig(section, key):
    config = configparser.ConfigParser()
    config.read(configPath)
    return config.get(section, key)



# if __name__=="__main__":
#     value = getConfig()
#     print(value)