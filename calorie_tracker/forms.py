from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextAreaField, SubmitField, DateField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, EqualTo
from wtforms.fields import DateTimeLocalField
import datetime

class LoginForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired(), Length(1, 100)])
    password = PasswordField('密碼', validators=[DataRequired()])
    submit = SubmitField('登入')

    
class RegisterForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])
    birthdate = DateField('生日', format='%Y-%m-%d', validators=[Optional()])
    gender = SelectField('性別', choices=[('男', '男'), ('女', '女'), ('其他', '其他')], validators=[Optional()])
    height = FloatField('身高 (cm)', validators=[Optional()])
    weight = FloatField('體重 (kg)', validators=[Optional()])

    username = StringField('帳號', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('密碼', validators=[DataRequired(), Length(min=3, max=150)])
    confirm_password = PasswordField('確認密碼', validators=[DataRequired(), EqualTo('password', message='兩次密碼需一致')])
    submit = SubmitField('註冊')

class FoodForm(FlaskForm):
    name = StringField('食品名稱', validators=[DataRequired()])
    type = StringField('食品類型')
    calories = FloatField('卡路里')
    location = StringField('販售地點')
    submit = SubmitField('新增食品')


class DietRecordForm(FlaskForm):
    timestamp = DateTimeLocalField(
        '進食時間',
        format='%Y-%m-%dT%H:%M:%S',  # 對應 HTML datetime-local 格式
        default=datetime.datetime.now,
        validators=[DataRequired()]
    )
    food_name = StringField('食品名稱', validators=[DataRequired(message='必填')])
    food_type = StringField('食品類型')
    calories = FloatField('卡路里', validators=[DataRequired(message='必填')])
    location = StringField('販售地點')
    notes = TextAreaField('備註')
    add_to_food = BooleanField('添加至食品管理')
    submit = SubmitField('新增紀錄')

    
class EditDietRecordForm(FlaskForm):
    timestamp = DateTimeLocalField('進食時間', format='%Y-%m-%dT%H:%M:%S', validators=[DataRequired(message='必填')])
    food_name = StringField('食品名稱', validators=[DataRequired(message='必填')])
    food_type = StringField('食品類型')
    calories = FloatField('卡路里', validators=[DataRequired(message='必填'), NumberRange(min=0)])
    location = StringField('販售地點')
    notes = TextAreaField('備註')
    submit = SubmitField('儲存修改')
    
    
class UpdateProfileForm(FlaskForm):
    name = StringField('姓名', validators=[Optional()])
    birthdate = DateField('生日', format='%Y-%m-%d', validators=[Optional()])
    gender = SelectField('性別', choices=[('男', '男'), ('女', '女'), ('其他', '其他')], validators=[Optional()])
    height = FloatField('身高 (cm)', validators=[Optional()])
    weight = FloatField('體重 (kg)', validators=[Optional()])
    profile_submit = SubmitField('更新資料')
    
class UpdateAccountForm(FlaskForm):
    current_password = PasswordField('原密碼', validators=[DataRequired()])
    new_username = StringField('新帳號', validators=[Optional(), Length(min=3, max=150)])
    new_password = PasswordField('新密碼', validators=[Optional()])
    confirm_new_password = PasswordField('確認新密碼', validators=[Optional(), EqualTo('new_password', message='兩次密碼需一致')])
    account_submit = SubmitField('更新帳號密碼')
