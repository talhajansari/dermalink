from app import app, db, lm, bcrypt
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flaskext.uploads import UploadSet, configure_uploads, IMAGES
from forms import LoginForm, SignupForm
from models import User, Image

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
	loginForm = LoginForm()
	signupForm = SignupForm()
	return render_template("index.html", title = 'Log in', form1=loginForm, form2=signupForm)

@app.route("/login", methods=["POST"])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	loginForm = LoginForm()
	signupForm = SignupForm()
	if loginForm.validate_on_submit():
		email = loginForm.email.data
		password = loginForm.password.data
		if email is None or password is None:
			flash('Invalid login. Please try again.')
			return redirect(url_for('index'))
		user = User.query.filter_by(email = email).first()
		if user is None:
			flash('That email does not exist. Please try again.')
			return redirect(url_for('index'))
		if bcrypt.check_password_hash(user.password, password) is False:
			flash('Invalid Login. Please try again.')
			return redirect(url_for('index'))
		login_user(user, remember=True)
		#return redirect(request.args.get("next") or url_for("user", email=user.email, user=user))
		return redirect(url_for("upload"))
	return render_template("index.html", title = 'Sign In', form1=loginForm, form2=signupForm)

@app.route("/signup", methods=["POST"])
def signup():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	loginForm = LoginForm
	signupForm = SignupForm()
	if signupForm.validate_on_submit():
		email = signupForm.email.data
		if email not in reserved_usernames.split():
			password = signupForm.password.data
			password_hash = bcrypt.generate_password_hash(password)
			user = User.query.filter_by(email = email).first() # Check if that email already exists
			if user is not None:
				flash('That email is already in use')
				return redirect(url_for('index'))
			
			# Create the user
			user = User(password=password_hash, email=email)
			db.session.add(user)
			db.session.commit()
		login_user(user, remember=True)
		#return redirect(request.args.get("next") or url_for("editProfile", username=user.username, user=user))
		return redirect(url_for("upload"))
	return render_template("index.html", title = 'Sign Up', form1=loginForm, form2=signupForm)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	form = LoginForm()
	return redirect("/")

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
	if request.method == 'POST' and 'image' in request.files:
		filename = images.save(request.files['image'])
		image = Image(filename=filename, user=g.user)
		db.session.add(image)
		db.session.commit()
		return redirect(url_for('show', id=image.id))
	return render_template('upload.html')

@app.route('/image/<id>')
@login_required
def show(id):
	image = Image.query.get(id)
	if image is None:
		abort(404)
	url = images.url(image.filename)
	return render_template('show.html', url=url, image=image)



