from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError, InputRequired, email, Length
from werkzeug.security import generate_password_hash

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username is required.")])
    password = PasswordField('Password', validators=[ InputRequired(message="Password is required."),
        Length(min=6, message="Password must be at least 6 characters long.")])
    confirm_password = PasswordField('Confirm password', validators=[ InputRequired(message="Password is required.")])
    email = EmailField('email', validators=[
        InputRequired(message="Email is required.")])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign up')
    
class LoginForm(FlaskForm):
    email = EmailField('email', validators=[
        InputRequired(message="Email is required."),
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    password = PasswordField('Password', validators=[ InputRequired(message="Password is required.")])
    submit = SubmitField('Log in')
    remember_me = BooleanField('Remember me')
    
class AddBlogForm(FlaskForm):
    title = StringField('Blog Title', validators=[InputRequired(message= "Can't be empty")])
    content = TextAreaField('Content', validators=[InputRequired(message="Can't be empty")])
    image = FileField('Upload title picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'webp', 'jpeg'])])
    submit = SubmitField('Update')