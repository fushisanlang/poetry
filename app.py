#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 下午10:21
# @Author  : fushisanlang
# @File    : app.py
# @Software: PyCharm
from flask import Flask, request, redirect, url_for, render_template,flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User, query_user
from operate_data import select_operaction
import random
from fanjian import fanToJian
from restr import reStr
import json

app = Flask(__name__)
app.secret_key = '1234567'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user

@app.route('/',methods=['POST', 'GET'])
@login_required
def index():
    return 'Logged in as: %s' % current_user.get_id()

@app.route('/tangshi',methods=['POST', 'GET'])
@login_required
def tangshi():
    if request.method == 'POST':
        id = request.form.get('id')
        status = request.form.get('status')
        #print(id, status,current_user.get_id())
    max_id = select_operaction('max(id)', 'tangshi')[0][0]
    random_id = str((random.randint(0,max_id)))
    #random_id = "55762"
    where_value = "id = " + random_id
    R_str = select_operaction('*','tangshi',where_value)
    R_id = R_str[0][0]
    R_title = fanToJian(R_str[0][1].decode('UTF-8'))
    R_author = fanToJian(R_str[0][2].decode('UTF-8'))
    R_paragraphs = reStr(fanToJian(R_str[0][3].decode('UTF-8'))).split('\n')
    return render_template('tangshi.html',
                           id = R_id,title = R_title,author = R_author,paragraphsList = R_paragraphs)

@app.route('/songshi',methods=['POST', 'GET'])
def songshi():
    return render_template('songshi.html')

@app.route('/songci',methods=['POST', 'GET'])
def songci():
    if request.method == 'POST':
        id = request.form.get('id')
        status = request.form.get('status')
        print(id, status,current_user.get_id())
    return render_template('songci.html')

@app.route('/lunyu')
def lunyu():
    return render_template('lunyu.html')

@app.route('/shijing')
def shijing():
    return render_template('shijing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        G_username= request.form.get('username')
        G_userpass= request.form.get('userpass')
        S_user_str = query_user(G_username)
        if S_user_str is None:
            return render_template('login_error.html')
        # print(S_user_str)
        S_username = S_user_str[0][1].decode('UTF-8')
        # print(S_username)
        # print(G_username)
        S_userpass = S_user_str[0][2].decode('UTF-8')
        # print(S_userpass)
        # print(G_userpass)
        if G_username is not None and G_userpass == S_userpass:

            curr_user = User()
            curr_user.id = G_username
            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)
            return redirect(url_for('index'))
        else:
            return render_template('login_error.html')
            flash('Wrong username or password!')
    # GET 请求
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_success', methods=['POST'])
def register_success():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)