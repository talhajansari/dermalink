from app import app, db, lm, bcrypt
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flaskext.uploads import UploadSet, configure_uploads, IMAGES
from forms import LoginForm, SignupForm, CreateIssueForm, DermSignupForm
from models import User, Image, Issue, Patient, Doctor
from datetime import datetime

reserved_usernames = 'home signup login logout post'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request   
def before_request():
	g.user = current_user


@app.route('/')
@app.route('/index')
def index():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for("home"))
	else:
		loginForm = LoginForm()
		signupForm = SignupForm()
		derm_signupForm = DermSignupForm()
		return render_template("index.html", title = 'Log in', form1=loginForm, form2=signupForm, form3=derm_signupForm)


@app.route("/login", methods=["POST"])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('home'))
	loginForm = LoginForm()
	signupForm = SignupForm()
	derm_signupForm = DermSignupForm()
	if loginForm.validate_on_submit():
		email = loginForm.email.data
		password = loginForm.password.data
		if email is None or password is None:
			flash('Invalid login. Please try again.')
			return redirect(url_for('index'))
		user = User.query.filter_by(email = email).first()
		if user is None: # and dermatologist is None:
			flash('That email does not exist. Please try again.')
			return redirect(url_for('index'))
		if user is not None:
			if bcrypt.check_password_hash(user.password, password) is False:
				flash('Invalid Login. Please try again.')
				return redirect(url_for('index'))
			login_user(user, remember=True)
			return redirect(url_for("home"))
	return render_template("index.html", title = 'Sign In', form1=loginForm, form2=signupForm, form3=derm_signupForm)


@app.route("/signup", methods=["POST"])
def signup():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('home'))
	loginForm = LoginForm()
	signupForm = SignupForm()
	derm_signupForm = DermSignupForm()
	if signupForm.validate_on_submit():
		email = signupForm.email.data
		if email not in reserved_usernames.split():
			password = signupForm.password.data
			password_hash = bcrypt.generate_password_hash(password)
			user = User.query.filter_by(email = email).first() # Check if that email already exists
			#if dermatologist is not None or user is not None:
			if user is not None:
				flash('That email is already in use')
				return redirect(url_for('index'))			
			# Create the user
			user = User(password=password_hash, email=email, isDoctor=0)
			db.session.add(user)
			db.session.flush()
			patient = Patient(user_id=user.id)
			db.session.add(patient)
			db.session.flush()
			user.patient = patient
			db.session.flush()
			db.session.commit()
		login_user(user, remember=True)
		#return redirect(request.args.get("next") or url_for("editProfile", username=user.username, user=user))
		return redirect(url_for("home"))
	return render_template("index.html", title = 'Sign Up', form1=loginForm, form2=signupForm, form3=derm_signupForm)


@app.route("/derm_signup", methods=["POST"])
def derm_signup():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('issues'))
	loginForm = LoginForm()
	signupForm = SignupForm()
	derm_signupForm = DermSignupForm()
	if derm_signupForm.validate_on_submit():
		email = derm_signupForm.email.data
		if email not in reserved_usernames.split():
			password = derm_signupForm.password.data
			password_hash = bcrypt.generate_password_hash(password)
			user = User.query.filter_by(email = email).first() # Check if that email already exists
			#if dermatologist is not None or user is not None:
			if user is not None:
				flash('That email is already in use')
				return redirect(url_for('index'))
			doctor = Doctor()
			db.session.add(doctor)
			user = User(password=password_hash, email=email, isDoctor=1, doctor=doctor)
			db.session.add(user)
			db.session.commit()
		login_user(user, remember=True)
		#return redirect(request.args.get("next") or url_for("editProfile", username=user.username, user=user))
		#return redirect(url_for("derm_home"))
		return redirect(url_for("home"))
	return render_template("index.html", title = 'Sign Up', form1=loginForm, form2=signupForm, form3=derm_signupForm)


@app.route('/home')
@login_required
def home():
	createIssueForm = CreateIssueForm()
	if not g.user.isDoctor==1: #is not doctor
		issues = Issue.query.filter_by(patient_id=g.user.patient.id) 
		return render_template('issues.html', issues=issues, isDoctor=0, form1=createIssueForm)
	elif g.user.isDoctor:
		doctor_id = g.user.doctor.id
		#return str(g.user.doctor.isAvailableMethod())
		#issues = Issue.query.filter_by(doctor_id=g.user.doctor.id)
		issues = Issue.query.filter(Issue.doctors.any(id=doctor_id)).all()
		return render_template('issues.html', issues=issues, isDoctor=1, form1=createIssueForm)


@app.route('/create', methods=['POST'])
@login_required
def create_issue():
	createIssueForm = CreateIssueForm()
	if createIssueForm.validate_on_submit():
		summary = createIssueForm.summary.data
		user_id = g.user.id
		patient_id = g.user.patient.id
		issue = Issue(summary=summary, timestamp= datetime.utcnow(), patient_id=patient_id, isClosed=0)
		db.session.add(issue)
		db.session.flush()
		assignIssueToDoctor(issue)
		db.session.commit()
		issue_id = issue.id
		return redirect(url_for('upload', issue_id=issue_id))


@app.route('/home/<id>')
@login_required
def show_issue(id):
	if not g.user.isDoctor:
		authenticate = g.user.patient.owns_issue(id)
	elif g.user.isDoctor:
		authenticate = g.user.doctor.owns_issue(id)
	if authenticate is False:
		return redirect(url_for("home"))
	issue = Issue.query.get(id)
	if issue is None:
		return 'No such issue found'
	pics = Image.query.filter_by(issue_id=id).all()
	URLs = []
	for image in pics:
		url = images.url(image.filename)
		URLs.append(url)
	return render_template('show_issue.html', issue=issue, URLs=URLs, images=images)


@app.route('/home/<issue_id>/upload', methods=['GET', 'POST'])
@login_required
def upload(issue_id):
	if request.method == 'POST' and 'image' in request.files:
		filename = images.save(request.files['image'])
		image = Image(filename=filename, issue_id=issue_id)
		db.session.add(image)
		db.session.commit()
		return redirect(url_for("show_issue", id=issue_id))
	issue = Issue.query.get(issue_id)
	#return str(issue.summary)
	return render_template('upload.html', issue=issue)


@app.route("/logout")
@login_required
def logout():
	logout_user()
	form = LoginForm()
	return redirect("/")


## Other functions

# For now, it only assigns the issues to the first dermatologist
def assignIssueToDoctor(issue):
	doctors = Doctor.query.filter_by(isAvailable=1).all()
	if len(doctors) is 0:
		doc = Doctor.query.first()
		doc.issues.append(issue)
		db.session.commit()
		return doc
	else:
		for doc in doctors:
			if doc.isAvailableMethod():
				doc.issues.append(issue)
				doc.isAvailableMethod()
				db.session.commit()
				return doc
