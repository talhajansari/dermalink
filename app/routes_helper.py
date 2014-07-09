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
from forms import LoginForm, SignupForm, ForgotPasswordForm, ChangePasswordForm, CreateIssueForm, DermSignupForm, EditProfileForm, DiagnosisForm, UploadImageForm
from flask.ext.wtf import Form
from wtforms import SelectField
from wtforms.ext.sqlalchemy.orm import model_form

# Communication
from flask.ext.mail import Message
from twilio.rest import TwilioRestClient
import stripe

# Python
import string
import random
import os

## VARIABLES ##

MAX_IMAGES = 5

# Routes variables
reserved_usernames = 'home signup login logout post'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

# Twilio Account Information
account = 'AC6056ccab9b128c038c932d4bbf81b662'
token = 'd6a72dff4e0f118e2e52d15ef51f4548'
client = TwilioRestClient(account, token)
MY_TWILIO_NUMBER = '+14408478798'

## FUNCTIONS ##

# Assign issue to dermatologists
def assignIssueToDoctor(issue):
	doctors = Doctor.query.filter_by(is_available=1, is_complete=1).all()
	if len(doctors) is 0: # No available doctors, just assign to the first doctor in the list?
		doc = Doctor.query.first()
		if doc is None:
			return None
		doc.issues.append(issue)
		db.session.flush()
		return doc
	else: # At least one doctor available
		diff = 0
		best_doc = None # Chose the best doc, based on availability etc.
		for doc in doctors:
			if doc.isAvailable() and (doc.issue_limit-doc.numOpenIssues())>=0 :
				best_doc = doc
		doc = best_doc		
		doc.issues.append(issue)
		doc.isAvailable()
		db.session.flush()
		return doc


# Routes Functions 
def SendSMS(number, body):
	# client.sms.messages.create(to=number, from_=MY_TWILIO_NUMBER, body=body)
	pass

def sendEmail(subject, body, recipients, sender='derMangoPlus@gmail.com'):
	# msg = Message(subject=subject,
 #                  sender=sender,
 #                  recipients=recipients)
	# msg.body = body
	# mail.send(msg)
	pass

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
	#flash('Succesfully logged out.')
	#form = LoginForm()
	return redirect("/")

@app.route("/admin")
def admin():
	from config import SQLALCHEMY_DATABASE_URI
	users = User.query.all()
	return render_template("admin.html", users=users, db_env_var = os.environ.get('DATABASE_URL'), sqlalchemy_uri=SQLALCHEMY_DATABASE_URI)

@app.route("/charge", methods=['POST'])
def charge():
	 # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email=g.user.email,
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )
    return "Succesfully charged"
