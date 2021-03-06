#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 下午10:21
# @Author  : fushisanlang
# @File    : app.py
# @Software: PyCharm
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User, query_user
from operate_data import select_operaction, insert_operaction
import random
from operate_str import reStr, fanToJian, deCodeList
import hashlib
import time

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


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    username = current_user.get_id()
    S_tangshi_keys = "ts.id,ts.title,ts.author"
    S_tangshi_tables = "tangshi_shoucang tss,user u ,tangshi ts "
    S_tangshi_values = "u.user = \"" + username + "\" and tss.user_id = u.id and ts.id = tss.from_id group by 1"
    S_tangshi_result = select_operaction(S_tangshi_keys,S_tangshi_tables,S_tangshi_values)
    S_tangshi_result = deCodeList(S_tangshi_result)
    return render_template('user.html', username=username,S_tangshi_result=S_tangshi_result,
                           type="tangshi")


@app.route('/<path:post_type>', methods=['POST', 'GET'])
@login_required
def songshi(post_type):
    if post_type == "tangshi":
        ZH_type = "唐诗"
    elif post_type == "songshi":
        ZH_type = "宋诗"
    elif post_type == "songci":
        ZH_type = "宋词"
    elif post_type == "shijing":
        ZH_type = "诗经"
    else:
        return redirect(url_for('index'))

    shoucang_str = post_type + "_shoucang"

    if request.method == 'POST':
        id = request.form.get('id')
        type = request.form.get('type')
        if type == "shoucang":
            shoucang_I_keys = "user_id,from_id"
            shoucang_User_values = "user = \"" + current_user.get_id() + "\""
            shoucang_User_id = select_operaction("id", "user", shoucang_User_values)[0][0]
            shoucang_I_values = "\"" + str(shoucang_User_id) + "\",\"" + id + "\""
            insert_operaction(shoucang_str, shoucang_I_keys, shoucang_I_values)
        if type == "yichang":
            yichang_I_keys = "type,from_id"
            yichang_I_values = "\"" + post_type + "\",\"" + id + "\""
            insert_operaction("yichang", yichang_I_keys, yichang_I_values)

    max_id = select_operaction('max(id)', post_type)[0][0]
    random_id = str((random.randint(0, max_id)))
    where_value = "id = " + random_id
    R_str = select_operaction('*', post_type, where_value)
    R_id = R_str[0][0]
    R_title = fanToJian(R_str[0][1].decode('UTF-8'))
    R_author = fanToJian(R_str[0][2].decode('UTF-8'))
    R_paragraphs = reStr(fanToJian(R_str[0][3].decode('UTF-8'))).split('\n')
    return render_template('read.html',
                           id=R_id, title=R_title, author=R_author, paragraphsList=R_paragraphs,
                           EN_type=post_type, ZH_type=ZH_type)

@app.route('/<path:post_type>/<int:post_id>')
@login_required
def show_post(post_type,post_id):
    if post_type == "tangshi":
        ZH_type = "唐诗"
    elif post_type == "songshi":
        ZH_type = "宋诗"
    elif post_type == "songci":
        ZH_type = "宋词"
    elif post_type == "shijing":
        ZH_type = "诗经"
    else:
        return redirect(url_for('index'))

    S_result = select_operaction("id,title,author,paragraphs", post_type, "id = " + str(post_id))
    S_id = S_result[0][0]
    S_title = fanToJian(S_result[0][1].decode('UTF-8'))
    S_author = fanToJian(S_result[0][2].decode('UTF-8'))
    S_paragraphs = reStr(fanToJian(S_result[0][3].decode('UTF-8'))).split('\n')
    print(S_result)
    return render_template('read_2.html',
                           id=S_id, title=S_title, author=S_author, paragraphsList=S_paragraphs,
                           EN_type=post_type,ZH_type=ZH_type)


#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        G_username = request.form.get('username')
        G_userpass = request.form.get('userpass')
        S_user_str = query_user(G_username)
        if S_user_str is None:
            return render_template('login_error.html')
        S_userpass_sha1 = S_user_str[0][2].decode('UTF-8')
        G_userpass_sha1 = hashlib.sha1(G_userpass.encode("utf-8")).hexdigest()
        if G_username is not None and G_userpass_sha1 == S_userpass_sha1:

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
    G_username = request.form.get('user')
    G_userpass = request.form.get('pass')
    G_userpass_2 = request.form.get('pass2')
    if G_username is None:
        R_message = "用户名为空，请重新注册"
        return render_template('register_error.html', R_message=R_message)
    S_user_str = query_user(G_username)
    if S_user_str is not None:
        R_message = "用户名已存在，请重新注册"
        return render_template('register_error.html', R_message=R_message)
    if G_userpass is None:
        R_message = "密码为空，请重新注册"
        return render_template('register_error.html', R_message=R_message)
    if G_userpass_2 != G_userpass:
        R_message = "两次密码不匹配，请重新注册"
        return render_template('register_error.html', R_message=R_message)
    I_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    I_pass_sha1 = hashlib.sha1(G_userpass.encode("utf-8")).hexdigest()
    I_keys = "user,pass,createtime"
    I_values = "\"" + G_username + "\",\"" + I_pass_sha1 + "\",\"" + I_time + "\""
    insert_operaction("user", I_keys, I_values)
    return render_template('register_success.html', username=G_username, password=G_userpass)


if __name__ == '__main__':
    app.run(debug=True)