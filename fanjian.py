#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 下午10:21
# @Author  : fushisanlang
# @File    : fanjian.py
# @Software: PyCharm
from opencc import OpenCC

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
