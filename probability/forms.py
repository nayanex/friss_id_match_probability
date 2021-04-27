from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class ProbabilityForm(FlaskForm):
    first_name1 = StringField("First name", validators=[DataRequired(), Length(0, 64)])
    last_name1 = StringField("Last Name", validators=[DataRequired(), Length(0, 64)])
    birth_date1 = StringField("Birth Date")
    bsn1 = StringField("Identification Number")
    first_name2 = StringField("First name", validators=[DataRequired(), Length(0, 64)])
    last_name2 = StringField("Last Name", validators=[DataRequired(), Length(0, 64)])
    birth_date2 = StringField("Birth Date")
    bsn2 = StringField("Identification Number")
    submit = SubmitField("Compute")
