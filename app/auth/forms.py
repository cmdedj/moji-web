from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
	email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
	password = PasswordField('密码', validators=[DataRequired()])
	remember_me = BooleanField('记得我')
	submit = SubmitField('登陆')


class RegistrationForm(Form):
	email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
	username = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只有字母，数字，点和下划线')])
	password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='密码不匹配')])
	password2 = PasswordField('确认密码', validators=[DataRequired()])
	submit = SubmitField('注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('电子邮件已经被注册')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已经被注册')


class ChangePasswordForm(Form):
	old_password = PasswordField('旧密码', validators=[DataRequired()])
	password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='密码不匹配')])
	password2 = PasswordField('确认新密码', validators=[DataRequired()])
	submit = SubmitField('更新密码')


class PasswordResetRequestForm(Form):
	email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
	submit = SubmitField('下一步')


class PasswordResetForm(Form):
	email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
	password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='密码不匹配')])
	password2 = PasswordField('确认新密码', validators=[DataRequired()])
	submit = SubmitField('重置密码')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('无效的电子邮件')


class ChangeEmailForm(Form):

	email = StringField('新电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
	password = PasswordField('密码', validators=[DataRequired()])
	submit = SubmitField('更新电子邮件')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('电子邮件已经被注册')
