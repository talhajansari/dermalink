# All non-route stuff is included in the file routes_helper
from routes_helper import *

 
# Routes...

@app.route('/')
@app.route('/index')
def index():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for("home"))
	else:
		loginForm = LoginForm()
		signupForm = SignupForm()
		derm_signupForm = DermSignupForm()
		return render_template("index_dlink.html", title = 'SkinCheck', form1=loginForm, form2=signupForm, form3=derm_signupForm)


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
			user = User(password=password_hash, email=email, role='PATIENT')
			db.session.add(user)
			db.session.flush()
			patient = Patient(user_id=user.id, isComplete = 0)
			db.session.add(patient)
			db.session.flush()
			user.patient = patient
			db.session.flush()
			db.session.commit()
		login_user(user, remember=True)
		#sendEmail('You have signed up!')
		#return redirect(request.args.get("next") or url_for("editProfile", username=user.username, user=user))
		return redirect(url_for("editProfile", id=user.id))
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
			if user is not None:
				flash('That email is already in use')
				return redirect(url_for('index'))
			# Create the user
			user = User(password=password_hash, email=email, role='DOCTOR')
			db.session.add(user)
			db.session.flush()
			doctor = Doctor(user_id=user.id, isComplete = 0)
			db.session.add(doctor)
			db.session.flush()
			user.doctor = doctor
			db.session.flush()
			db.session.commit()
		login_user(user, remember=True)
		#return redirect(request.args.get("next") or url_for("editProfile", username=user.username, user=user))
		return redirect(url_for("editProfile", id=user.id))
	return render_template("index.html", title = 'Sign Up', form1=loginForm, form2=signupForm, form3=derm_signupForm)

@app.route("/forgot_password", methods=["GET","POST"])
def forgot_password():
	form = ForgotPasswordForm()
	if form.validate_on_submit():
		email = form.email.data
		user = User.query.filter_by(email = email).first()
		if user is None:
			flash('This email does not exist. Please try again.')
			return redirect(url_for('forgot_password'))
		token = id_generator(size=8)
		token_user = TokenUser(token=token, user_id = user.id)
		db.session.add(token_user)
		#return token
		# Write an email
		subject = "DerMango | Forgot your password"
		body = 'Please click on the following link to reset your password: http://127.0.0.1:5000/forgot_password/'+str(token)
		sendEmail(subject, body, recipients=[email], sender='talhajansari@gmail.com')
		db.session.commit()
		flash('An email has been sent to your address with a password reset link.')
		return render_template("forgot_password.html", form=form)	
	return render_template("forgot_password.html", form=form)

@app.route("/forgot_password/<token>", methods=["GET", "POST"])
def change_password(token):
	form = ChangePasswordForm()
	token_user = TokenUser.query.filter_by(token = token).first()
	if token_user is None:
		flash('Incorrect URL. Send yourself a new URL, or try the old one again.')
		return redirect(url_for('forgot_password'))
	if request.method=="POST" and form.validate_on_submit():
		user = User.query.get(token_user.user_id)
		password = form.password.data
		password_hash = bcrypt.generate_password_hash(password)
		user.password = password_hash
		db.session.commit()
		db.session.delete(token_user)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("change_password.html", form=form, token=token)


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
		if user is None:
			flash('This email does not exist. Please try again.')
			return redirect(url_for('index'))
		if user is not None:
			if bcrypt.check_password_hash(user.password, password) is False:
				flash('Invalid password. Please try again.')
				return redirect(url_for('index'))
			login_user(user, remember=True)
			flash('Succesfully logged in.')	
			return redirect(url_for("home"))
	return render_template("index.html", title = 'Sign In', form1=loginForm, form2=signupForm, form3=derm_signupForm)


@app.route('/home')
@login_required
def home():
	createIssueForm = CreateIssueForm()
	if g.user.isPatient(): #is not doctor
		issues = Issue.query.filter_by(patient_id=g.user.patient.id) 
		complete = g.user.patient.isComplete()
		return render_template('home.html', issues=issues, isDoctor=0, isComplete=complete, form1=createIssueForm)
	elif g.user.isDoctor():
		doctor_id = g.user.doctor.id
		#is_complete = g.user.doctor.isComplete()
		issues = Issue.query.filter(Issue.doctors.any(id=doctor_id)).all()
		return render_template('home.html', issues=issues, isDoctor=1)



@app.route("/edit/<id>", methods=["POST", "GET"])
@login_required
def editProfile(id):
	user = User.query.get(id)
	if user == None:
		return redirect(url_for('home'))
	if g.user.id is not int(id):
		return redirect(url_for('home'))
	if g.user.isPatient():
		MyForm = model_form(Patient, Form, exclude=['issues', 'user', 'is_complete'])
		patient = g.user.patient
		form = MyForm(request.form, patient)
	if g.user.isDoctor():
		MyForm = model_form(Doctor, Form, exclude=['issues', 'diagnoses', 'user', 'is_complete', 'is_available','is_certified', 'rating'])
		#MyForm.gender = RadioField(choices=[('male', 'male'), ('female', 'female')])
		MyForm.issue_limit = SelectField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
		doctor = g.user.doctor
		form = MyForm(request.form, doctor)
		
	if request.method == 'POST':
		if g.user.isPatient(): #is not doctor
			form.populate_obj(patient)
			db.session.commit()
			return redirect(url_for('home'))
		elif g.user.isDoctor():
			#form = model_form(Doctor, exclude=['issues', 'diagnoses', 'user', 'is_complete', 'is_available','is_certified', 'rating'])(request.form)
			form.populate_obj(doctor)
			db.session.commit()
			doctor.isComplete()
			return redirect(url_for('home'))
	# elif request.method == 'GET':
	return render_template("edit_profile.html", form=form)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_issue():
	createIssueForm = CreateIssueForm()
	if request.method=='GET':
		return render_template('create_issue.html', form=createIssueForm)	
	if createIssueForm.validate_on_submit():
		summary = createIssueForm.summary.data
		#filename = secure_filename(createIssueForm.image.data.filename)
		filename = images.save(request.files['image'])
		#user_id = g.user.id
		patient_id = g.user.patient.id
		issue = Issue(summary=summary, timestamp= datetime.utcnow(), patient_id=patient_id, is_closed=0)
		db.session.add(issue)
		db.session.flush()
		image = Image(filename=filename, timestamp= datetime.utcnow(), issue_id=issue.id)
		createIssueForm.image.file.save('uploads/'+str(filename))
		db.session.add(image)
		db.session.flush()
		assignIssueToDoctor(issue)
		db.session.commit()
		issue_id = issue.id
		return redirect(url_for('show_issue', id=issue_id))


@app.route('/home/<id>', methods=['GET', 'POST'])
@login_required
def show_issue(id):
	form = DiagnosisForm()
	if request.method == 'POST': # Diagnose
		issue = Issue.query.get(id)
		summary = form.diagnosis.data
		diagnosis = Diagnosis(diagnosis=summary, doc_id=g.user.doctor.id, issue_id=id, timestamp= datetime.utcnow())
		db.session.add(diagnosis)
		issue.diagnoses.append(diagnosis)
		g.user.doctor.diagnoses.append(diagnosis)
		issue.is_closed = int(form.resolved.data)
		#return form.resolved.data
		db.session.commit()
		#send a message
		#SendSMS(issue.patient.phone, "SkinCheck: Your complaint, \'" + str(issue.summary) + "\', has been diagnosed by Dr. " + str(diagnosis.doctor.last_name) + ".")
		#msg = Message("Your complaint, \'" + str(issue.summary) + "\', has been diagnosed by Dr. " + str(diagnosis.doctor.lastName) + ".",
        #          sender="talhajansari+dermalink_sender@gmail.com",
        #          recipients=["talhajansari+dermalink_receiver@gmail.com"])
		return redirect(url_for('home'))
	# else if request.method = GET:
	issue = Issue.query.get(id)
	if g.user.isPatient():
		issues = Issue.query.filter_by(patient_id=g.user.patient.id)
		authenticate = g.user.patient.owns_issue(id)
	elif g.user.isDoctor():
		issues = Issue.query.filter(Issue.doctors.any(id=g.user.doctor.id)).all()
		authenticate = g.user.doctor.owns_issue(id)
	if authenticate is False:
		return redirect(url_for("home"))
	if issue is None: # will never reach this condition - can delete it
		return 'No such issue found'
	pics = Image.query.filter_by(issue_id=id).all()
	URLs = []
	for image in pics:
		url = images.url(image.filename)
		URLs.append(url)
	return render_template('show_issue.html', issue=issue, issues=issues, URLs=URLs, images=images, form=form)


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
	return render_template('upload.html', issue=issue)









