#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 下午10:21
# @Author  : fushisanlang
# @File    : operate_data.py
# @Software: PyCharm
import mysql.connector

def select_operaction(select_key,tablename,select_require="1"):
    conn = mysql.connector.connect(
        user="poetry", password="poetry", host="fushisanlang.cn", database="poetry"
    )
    cursor = conn.cursor()
    sql_parm1 = "SELECT "
    sql_parm2 = select_key
    sql_parm3 = " FROM "
    sql_parm4 = tablename
    sql_parm5 = " where "
    sql_parm6 = select_require
    sql_parm7 = ";"
    sql = sql_parm1 + sql_parm2 + sql_parm3 + sql_parm4 + sql_parm5 + sql_parm6 + sql_parm7
    #print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def insert_operaction(tablename,keys,valuses):
    conn = mysql.connector.connect(
        user="poetry", password="poetry", host="fushisanlang.cn", database="poetry"
    )
    cursor = conn.cursor()
    sql_parm1 = "INSERT INTO "
    sql_parm2 = tablename
    sql_parm3 = " (" + keys +")"
    sql_parm4 = " VALUES (" + valuses + ");"
    sql = sql_parm1 + sql_parm2 + sql_parm3 + sql_parm4
    #print(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    return

def update_operaction(tablename,update_str,key_str="1"):
    conn = mysql.connector.connect(
        user="poetry", password="poetry", host="fushisanlang.cn", database="poetry"
    )
    cursor = conn.cursor()
    sql_parm1 = "UPDATE "
    sql_parm2 = tablename
    sql_parm3 = " SET " + update_str +" WHERE "
    sql_parm4 = key_str + ";"
    sql = sql_parm1 + sql_parm2 + sql_parm3 + sql_parm4
    #print(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    return
