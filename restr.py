#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/18 上午10:54
# @Author  : fushisanlang
# @File    : restr.py
# @Software: PyCharm
import re
def reStr(strings):
    strings = strings
    value1 = re.sub("'\,\ '","\n",strings)
    value2 = re.sub("\[\'","",value1)
    value3 = re.sub("\'\]","",value2)

    return value3
