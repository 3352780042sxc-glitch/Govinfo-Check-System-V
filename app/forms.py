from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange

# 登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    role_id = SelectField('角色', coerce=int)
    submit = SubmitField('注册')

class InfoForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(min=2, max=200)])
    content = TextAreaField('内容', validators=[DataRequired()])
    category = StringField('类别', validators=[DataRequired(), Length(min=2, max=100)])
    status = SelectField('状态', choices=[('待审核', '待审核'), ('已发布', '已发布'), ('已归档', '已归档')], default='待审核')
    submit = SubmitField('提交')

# 数据抓取表单
class CrawlerForm(FlaskForm):
    keyword = StringField('搜索关键字', validators=[DataRequired(), Length(min=1, max=100)])
    quantity = IntegerField('数量', validators=[DataRequired(), NumberRange(min=1, max=100)], default=30)
    pages = IntegerField('页数', validators=[DataRequired(), NumberRange(min=1, max=10)], default=5)
    submit = SubmitField('开始采集')
