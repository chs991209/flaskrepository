from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('repassword')])
    repassword = PasswordField('repassword', validators=[DataRequired()])


class LoginForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])