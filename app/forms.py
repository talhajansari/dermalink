from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, FileField, TextAreaField, SelectField, HiddenField
from wtforms.validators import Required

class LoginForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class SignupForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])

class EditProfileForm(Form):
    password = PasswordField('password', id="form-field-pass1")
    confirmPassword = PasswordField('confirmPassword', id="form-field-pass2")

class CreateIssueForm(Form):
    summary = TextAreaField('summary', validators = [Required()])