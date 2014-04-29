from app import app, db, lm, bcrypt, mail
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flaskext.uploads import UploadSet, configure_uploads, IMAGES
from models import User, Image, Issue, Patient, Doctor, Diagnosis, TokenUser
from datetime import datetime
from werkzeug import secure_filename
from twilio.rest import TwilioRestClient
import twilio.twiml
# Forms
from forms import LoginForm, SignupForm, ForgotPasswordForm, ChangePasswordForm, CreateIssueForm, DermSignupForm, EditProfileForm, DiagnosisForm
from flask.ext.wtf import Form
from wtforms import SelectField
#from wtforms.validators import *
from wtforms.ext.sqlalchemy.orm import model_form
from flask.ext.mail import Message

import string
import random
import urllib