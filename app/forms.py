from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, FileField, TextAreaField, SelectField, HiddenField, RadioField
from wtforms.validators import Required

class LoginForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class SignupForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    #usertype = RadioField('usertype', validators = Required(), choices = ['Patient', 'Dermatologist']

class DermSignupForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])

class EditProfileForm(Form):
    password = PasswordField('password')
    confirmPassword = PasswordField('confirmPassword')
    firstName = TextField('firstName')
    lastName = TextField('lastName')
    gender = RadioField('gender', choices=[('male', 'male'), ('female', 'female')])
    age = TextField('age')
    ethnicity = TextField('ethnicity')
    hospital = TextField('hospital')
    city = TextField('city')
    state = TextField('state')
    country = TextField('country')

class CreateIssueForm(Form):
    summary = TextAreaField('summary', validators = [Required()])