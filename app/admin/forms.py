# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin, Tag

tags = Tag.query.all()


# 管理员登陆表单
class LoginForm(FlaskForm):
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号：",
            #    "required": "required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码：",
            #    "required": "required"
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",

        }
    )

    # 自定义验证器
    def validate_acccount(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在!")


# 标签表单
class TagForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入标签!")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary ",

        }
    )


# 添加电影
class MovieForm(FlaskForm):
    title = StringField(
        label="名称",
        validators=[
            DataRequired("请输入名称!")
        ],
        description="名称",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入名称"
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件!")
        ],
        description="文件",
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介!")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "row": 10
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面!")
        ],
        description="封面",
    )
    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级!")
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control",
        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签!")
        ],
        coerce=int,
        choices=[{v.id, v.name} for v in tags],
        description="标签",
        render_kw={
            "class": "form-control",
        }
    )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区!")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区"
        }
    )
    length = StringField(
        label="时长",
        validators=[
            DataRequired("请输入时长!")
        ],
        description="时长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入时长"
        }
    )
    release_time = StringField(
        label="时间",
        validators=[
            DataRequired("请输入时间!")
        ],
        description="时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入时间",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary ",
        }
    )

# 添加电影
class PreviewForm(FlaskForm):
    title= StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题!")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题"
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请上传预告封面!")
        ],
        description="预告封面",
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary ",

        }
    )

#修改密码
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码！",
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")

