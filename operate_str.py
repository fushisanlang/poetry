#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 下午10:21
# @Author  : fushisanlang
# @File    : operate_str.py
# @Software: PyCharm
from opencc import OpenCC
import re

def fanToJian(strings):
    #繁体 to 简体
    strings=strings
    strings=str(strings)
    return (OpenCC('t2s').convert(strings))

def jianToTan(strings):
    strings = strings
    #简体 to 繁体
    strings=str(strings)
    return (OpenCC('s2t').convert(strings))
#正则替换
def reStr(strings):
    strings = strings
    value1 = re.sub("'\,\ '","\n",strings)
    value2 = re.sub("\[\'","",value1)
    value3 = re.sub("\'\]","",value2)

    return value3

def deCodeList(lists):
    new_list = []
    for line in lists:
        id = line[0]
        title = fanToJian(line[1].decode('UTF-8'))
        author = fanToJian(line[2].decode('UTF-8'))
        new_tuple = (id,title,author)

        new_list.append(new_tuple)
    return new_list