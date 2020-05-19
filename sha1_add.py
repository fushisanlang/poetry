#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/20 上午3:05
# @Author  : fushisanlang
# @File    : sha1_add.py
# @Software: PyCharm
import hashlib

def sha1Add (pass_str):
    return_str = hashlib.sha1(pass_str.encode("utf-8")).hexdigest()
    return return_str
