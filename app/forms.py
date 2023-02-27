from unicodedata import category
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField, StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User, Post


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    mobile = StringField("Mobile", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat password", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("Username is already taken")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError("Email is already taken")

    def validate_mobile(self, mobile):
        user = User.query.filter_by(mobile = mobile.data).first()
        if user is not None:
            raise ValidationError("Mobile number is already taken")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = StringField("Details", validators=[DataRequired()])
    category = SelectField('Category', choices=[(1, "AEG"), (2,"GBB"), (3, "Sniper")])
    price = IntegerField("Price", validators=[DataRequired()])
    PSC = StringField("PSČ", validators=[DataRequired()])
    submit = SubmitField("Submit")
