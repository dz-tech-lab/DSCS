from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError


class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    user_handle = StringField("User Name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class LoginForm(FlaskForm):
    user_handle = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class PostForm(FlaskForm):
    content = StringField("Tweet", validators=[DataRequired(), Length(max=140)])
    submit_button = SubmitField("Tweet")
