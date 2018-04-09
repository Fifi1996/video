#coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/video"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')  #评论外键关系关联
    moviecols = db.relationship('Moviecol', backref='user')  # 电影收藏外键关系关联

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录ip地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签表
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    movies = db.relationship("Movie", backref="tag")  # 电影外键关联

    def __repr__(self):
        return "<Tag %r>" % self.id


# 电影表
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 播放地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id")) #所属标签
    area = db.Column(db.String(255)) # 地区
    release_time = db.Column(db.DateTime) # 时间
    length = db.Column(db.String(255)) # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    comments=db.relationship("Comment", backref="movie") #评论外键关联
    moviecols = db.relationship("Moviecol", backref="movie")#电影收藏外键关联

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title

# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    def __repr__(self):
        return "<Comment %r>" % self.id

#电影收藏
class Moviecol(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    def __repr__(self):
        return "<Moviecol %r>" % self.id

#权限表
class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    def __repr__(self):
        return "<Auth %r>" % self.name

#角色表
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    auths=db.Column(db.String(500)) #角色权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    admins=db.relationship("Admin", backref="role")  #管理员外键关联
    def __repr__(self):
        return "<Role %r>" % self.id

#管理员表
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账户
    pwd = db.Column(db.String(100)) #管理员密码
    is_super = db.Column(db.SmallInteger)#是否为超级管理员
    role_id=db.Column(db.Integer,db.ForeignKey("role.id")) #所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    adminlogs=db.relationship("Adminlog", backref="admin") #管理员登录日志外键关联
    oplogs=db.relationship("Oplog", backref="admin") #操作日志外键关联
    def __repr__(self):
        return "<Admin %r>" % self.name

#管理员登录表
class Adminlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id")) #所属管理员
    ip = db.Column(db.String(100))  # 登录ip地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加登录时间
    def __repr__(self):
        return "<Adminlog %r>" % self.name

#操作日志表
class Oplog(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    ip = db.Column(db.String(100))  # 登录ip地址
    reason=db.Column(db.String(500)) #操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加登录时间
    def __repr__(self):
        return "<Oplog %r>" % self.id

if __name__=="__main__":
    #db.create_all()
   from werkzeug.security import generate_password_hash  #哈希加密
   admin=Admin(
        name="001",
        pwd=generate_password_hash("123456"),
        is_super=0,
        role_id=1
    )
   #  role=Role(
   #      name="超级",
   #      auths=""
   #  )
   db.session.add(admin)
   db.session.commit()