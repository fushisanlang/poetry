#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 下午10:21
# @Author  : fushisanlang
# @File    : models.py
# @Software: PyCharm
from flask_login import UserMixin
from operate_data import select_operaction

class User(UserMixin):
    pass

users = [
    {'id':'fu', 'username': 'fu13', 'password': '1'},
    {'id':'qiecho', 'username': 'qiecho', 'password': '2'}
]

def query_user(user_name):
    user_select = "user = \"" + user_name + "\""
    user_str = select_operaction("id,user,pass,admin", "user", user_select)
    try:
        S_user = user_str[0]
    except :
        return
    else:
        return user_str

