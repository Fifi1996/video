from . import home
from flask import render_template,redirect,url_for
import os

#登陸
@home.route("/login/")
def login():
    return render_template("home/login.html")
#退出
@home.route("/logout/")
def logout():
    return redirect(url_for("home.login"))
#注冊
@home.route("/regist/")
def regist():
    return render_template("home/regist.html")
#會員中心
@home.route("/user/")
def user():
    return render_template("home/user.html")
#密碼
@home.route("/pwd/")
def pwd():
    return render_template("home/pwd.html")
#評論記録
@home.route("/comments/")
def comments():
    return render_template("home/comments.html")
#登録日誌
@home.route("/loginlog/")
def loginlog():
    return render_template("home/loginlog.html")
#收藏
@home.route("/moviecol/")
def moviecol():
    return render_template("home/moviecol.html")
#列表
@home.route("/")
def index():
    return render_template("home/index.html")
#動畫
@home.route("/animation/")
def animation():
    return render_template("home/animation.html")
#搜索
@home.route("/search/")
def search():
    return render_template("home/search.html")
#詳情
@home.route("/play/")
def play():
    return render_template("home/play.html")


