from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	password = db.Column(db.String(64), index = False, unique = False)
	email = db.Column(db.String(120), index = True, unique = True)
	gender = db.Column(db.String(12), index = True, unique = False)
	age = db.Column(db.Integer(3), index = True, unique = False)
	ethnicity = db.Column(db.String(120), index = True, unique = False)
	issues = db.relationship('Issue', backref='user', lazy='dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.username)

# Set of images pertaining to a single issue
class Issue(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	images = db.relationship('Image', backref='issue', lazy='dynamic')
	summary = db.Column(db.String(64), index = False, unique = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# An image within an issue
class Image(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	filename = db.Column(db.String(64), index = False, unique = True)
	label = db.Column(db.String(64), index = False, unique = False)
	issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))







