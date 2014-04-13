from app import db
import time
import datetime



doc_table = db.Table('doc_table',
	db.Column('doc_id', db.Integer, db.ForeignKey('doctor.id')),
	db.Column('issue_id', db.Integer, db.ForeignKey('issue.id'))
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	password = db.Column(db.String(64), index = False, unique = False)
	email = db.Column(db.String(120), index = True, unique = True)
	isDoctor = db.Column(db.Boolean, )
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
	# Relationships
	patient = db.relationship('Patient', backref='user', uselist=False)
	doctor = db.relationship('Doctor', backref='user', uselist=False)
	#issues = db.relationship('Issue', backref='user', lazy='dynamic')

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


class Patient(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	# Relationships
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	issues = db.relationship('Issue', backref='patient', lazy='dynamic')

	def owns_issue(self, id):
		issue = Issue.query.get(id)
		if issue.patient == self:
			return True
		else:
			return False

class Doctor(db.Model):
	id = db.Column(db.Integer, primary_key = True)	
	# Certification information
	isCertified = db.Column(db.Boolean, index = True, unique=False)
	isAvailable = db.Column(db.Boolean, index = True, unique=False)
	# Address fields
	hospital = db.Column(db.String(120), index = True, unique = False) # which hospital does the doctor practice?
	city = db.Column(db.String(120), index = True, unique = False)
	state = db.Column(db.String(120), index = True, unique = False) # or Province
	country = db.Column(db.String(120), index = True, unique = False)
	# Relationships
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	issues = db.relationship('Issue', secondary=doc_table, backref=db.backref('doctors', lazy='dynamic')) 

	def owns_issue(self, id):
		authenticate = False
		doctor_id = self.id
		assignedIssues = Issue.query.filter(Issue.doctors.any(id=doctor_id)).all()
		for issue in assignedIssues:
			if int(issue.id)==int(id):
				authenticate = True
		return authenticate

# Set of images pertaining to a single issue
class Issue(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	summary = db.Column(db.String(64), index = False, unique = False)
	# # Need to keep more information about the issue
	timestamp = db.Column(db.DateTime, index = False, unique = False) # when was the issue created online
	# howOld = db.Column(db.Integer(2), index = False, unique = False) # how many weeks old is the 'issue'
	isClosed = db.Column(db.Boolean, index = False, unique = False) # has the 'issue' been resolved?
	# Relationships
	#user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
	images = db.relationship('Image', backref='issue', lazy='dynamic')

# An image within an issue
class Image(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	filename = db.Column(db.String(64), index = False, unique = True) # why is the filename unique?
	label = db.Column(db.String(64), index = False, unique = False)
	date = db.Column(db.DateTime, index = False, unique = False)
	timestamp = db.Column(db.DateTime)
	issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))

	




