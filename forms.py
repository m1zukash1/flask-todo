from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from models import User

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=40)], render_kw={"placeholder": "Password"})
    email = StringField(validators=[InputRequired(), Email(), Length(max=60)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Register")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("That email is already registered!")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=40)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class TodoForm(FlaskForm):
    content = StringField(validators=[InputRequired(), Length(max=4000)], render_kw={"placeholder": "Enter your task"})
    submit = SubmitField("Submit Task")
