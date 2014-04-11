from app import db
import time
import datetime

derm_table = db.Table('derm_table',
	db.Column('dermatologist_id', db.Integer, db.ForeignKey('dermatologist.id')),
	db.Column('issue_id', db.Integer, db.ForeignKey('issue.id'))
)


class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	password = db.Column(db.String(64), index = False, unique = False)
	email = db.Column(db.String(120), index = True, unique = True)
	# Profile information
	firstName = db.Column(db.String(120), index = True, unique = False)
	lastName = db.Column(db.String(120), index = True, unique = False)
	gender = db.Column(db.String(12), index = True, unique = False)
	age = db.Column(db.Integer, index = True, unique = False)
	# Address fields
	city = db.Column(db.String(120), index = True, unique = False)
	state = db.Column(db.String(120), index = True, unique = False)
	zipcode = db.Column(db.Integer, index = True, unique = False)
	country = db.Column(db.String(120), index = True, unique = False)
	# Others
	ethnicity = db.Column(db.String(120), index = True, unique = False) # Should be optional - legal issues(?) if we force users to reveal this information
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
		return '<User %r>' % (self.email)

	def owns_issue(self, id):
		issue = Issue.query.get(id)
		if issue.user == self:
			return True
		else:
			return False

# Set of images pertaining to a single issue
class Issue(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	summary = db.Column(db.String(64), index = False, unique = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	# # Need to keep more information about the issue
	timestamp = db.Column(db.DateTime, index = False, unique = False) # when was the issue created online
	# howOld = db.Column(db.Integer(2), index = False, unique = False) # how many weeks old is the 'issue'
	isClosed = db.Column(db.Boolean, index = False, unique = False) # has the 'issue' been resolved?
	# Relationships
	images = db.relationship('Image', backref='issue', lazy='dynamic')

# An image within an issue
class Image(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	filename = db.Column(db.String(64), index = False, unique = True) # why is the filename unique?
	label = db.Column(db.String(64), index = False, unique = False)
	date = db.Column(db.DateTime, index = False, unique = False)
	timestamp = db.Column(db.DateTime)
	issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))


# Do we want it to be a sub-class of Users? I think not.
# Dermatologists (doctors) who view and respond to an issue 
class Dermatologist(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	password = db.Column(db.String(64), index = False, unique = False)
	email = db.Column(db.String(120), index = True, unique = True)
	# Profile information
	firstName = db.Column(db.String(120), index = True, unique = False)
	lastName = db.Column(db.String(120), index = True, unique = False)
	gender = db.Column(db.String(12), index = True, unique = False)
	age = db.Column(db.Integer, index = True, unique = False)
	# Certification information
	# <some fields regarding their medical education, degree, certification etc.>
	isCertified = db.Column(db.Boolean, index = True, unique=False)
	# Address fields
	hospital = db.Column(db.String(120), index = True, unique = False) # which hospital does the doctor practice?
	city = db.Column(db.String(120), index = True, unique = False)
	state = db.Column(db.String(120), index = True, unique = False) # or Province
	country = db.Column(db.String(120), index = True, unique = False)

	# Relationships
	issues = db.relationship('Issue', secondary=derm_table, backref=db.backref('dermatologists', lazy='dynamic')) 

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<Dermatologist %r>' % (self.email)
	




