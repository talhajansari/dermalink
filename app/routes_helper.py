## IMPORTS ##

# Basic Flask App imports
from app import app, db, lm, bcrypt, mail
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flaskext.uploads import UploadSet, configure_uploads, IMAGES
from models import User, Image, Issue, Patient, Doctor, Diagnosis, TokenUser
from datetime import datetime
from werkzeug import secure_filename

# Forms
from forms import LoginForm, SignupForm, ForgotPasswordForm, ChangePasswordForm, CreateIssueForm, DermSignupForm, EditProfileForm, DiagnosisForm
from flask.ext.wtf import Form
from wtforms import SelectField
from wtforms.ext.sqlalchemy.orm import model_form

# Communication
from flask.ext.mail import Message
from twilio.rest import TwilioRestClient

# Python
import string
import random

## VARIABLES ##

# Routes variables
reserved_usernames = 'home signup login logout post'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

# Twilio Account Information
# account = 'AC6056ccab9b128c038c932d4bbf81b662'
# token = 'd6a72dff4e0f118e2e52d15ef51f4548'
# client = TwilioRestClient(account, token)
# MY_TWILIO_NUMBER = '+14408478798'

## FUNCTIONS ##

# Assign issue to dermatologists
def assignIssueToDoctor(issue):
	doctors = Doctor.query.filter_by(is_available=1, is_complete=1).all()
	if len(doctors) is 0: # No available doctors
		doc = Doctor.query.first()
		doc.issues.append(issue)
		db.session.commit()
		return doc
	else: # At least one doctor available
		for doc in doctors:
			if doc.isAvailable():
				doc.issues.append(issue)
				doc.isAvailable()
				db.session.commit()
				# Send SMS notification
				#SendSMS(doc.phone, "SkinCheck: You have been assigned a new issue to diagnose")
				# Write an email
				email = doc.user.email
				subject = "SkinCheck | New Case"
				body = 'You have been assigned a new case. Please log on to SkinCheck to offer your diagnosis.'
				sendEmail(subject, body, recipients=[email], sender='dermaplus.skincheck@gmail.com')
				return doc


# Routes Functions 
def SendSMS(number, body):
	client.sms.messages.create(to=number, from_=MY_TWILIO_NUMBER, body=body)

def sendEmail(subject, body, recipients, sender='derMangoPlus@gmail.com'):
	msg = Message(subject=subject,
                  sender=sender,
                  recipients=recipients)
	msg.body = body
	mail.send(msg)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# Login-Authentication Functions
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request   
def before_request():
	g.user = current_user

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash('Succesfully logged out.')
	#form = LoginForm()
	return redirect("/")