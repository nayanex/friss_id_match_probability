from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ProbabilityForm(FlaskForm):
    first_name1 = StringField('First name', validators=[DataRequired(), Length(0, 64)])
    last_name1 = StringField('Last Name', validators=[DataRequired(), Length(0, 64)])
    birth_date1 = DateField('Birth Date', format='%Y-%m-%d')
    bsn1 = StringField('Identification Number')
    first_name2 = StringField('First name', validators=[DataRequired(), Length(0, 64)])
    last_name2 = StringField('Last Name', validators=[DataRequired(), Length(0, 64)])
    birth_date2 = DateField('Birth Date', format='%Y-%m-%d')
    bsn2 = StringField('Identification Number')
    probability = IntegerField("Matching Result")
    submit = SubmitField('Compute')