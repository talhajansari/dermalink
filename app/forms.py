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
    issueLimit = SelectField('issueLimit', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])


class CreateIssueForm(Form):
    summary = TextAreaField('summary', validators = [Required()])

class DiagnosisForm(Form):
    diagnosis = TextAreaField('diagnosis', validators = [Required()])
    hidden = HiddenField('hidden')