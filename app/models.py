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
	
	# Relationships
	patient = db.relationship('Patient', backref='user', uselist=False)
	doctor = db.relationship('Doctor', backref='user', uselist=False)

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
	isComplete = db.Column(db.Boolean()) # is profile complete
	firstName = db.Column(db.String(120), index = True, unique = False)
	lastName = db.Column(db.String(120), index = True, unique = False)
	gender = db.Column(db.String(12), index = True, unique = False)
	age = db.Column(db.Integer, index = True, unique = False)
	ethnicity = db.Column(db.String(120), index = True, unique = False)

	def owns_issue(self, id):
		issue = Issue.query.get(id)
		if issue.patient == self:
			return True
		else:
			return False

class Doctor(db.Model):
	id = db.Column(db.Integer, primary_key = True)	
	# Certification information
	isComplete = db.Column(db.Boolean()) # is profile complete
	isCertified = db.Column(db.Boolean, index = True, unique=False)
	isAvailable = db.Column(db.Boolean, index = True, unique=False)
	firstName = db.Column(db.String(120), index = True, unique = False)
	lastName = db.Column(db.String(120), index = True, unique = False)
	# Address fields
	hospital = db.Column(db.String(120), index = True, unique = False) # which hospital does the doctor practice?
	city = db.Column(db.String(120), index = True, unique = False)
	state = db.Column(db.String(120), index = True, unique = False) # or Province
	country = db.Column(db.String(120), index = True, unique = False)
	# Relationships
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	issues = db.relationship('Issue', secondary=doc_table, backref=db.backref('doctors', lazy='dynamic')) 
	# Number of issues they are willing to have at a time
	issueLimit = db.Column(db.Integer())
	diagnoses = db.relationship('Diagnosis', backref='doctor', lazy='dynamic')

	def owns_issue(self, id):
		authenticate = False
		doctor_id = self.id
		assignedIssues = Issue.query.filter(Issue.doctors.any(id=doctor_id)).all()
		for issue in assignedIssues:
			if int(issue.id) is int(id):
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
	patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
	images = db.relationship('Image', backref='issue', lazy='dynamic')
	diagnoses = db.relationship('Diagnosis', backref='issue', lazy='dynamic')

# An image within an issue
class Image(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	filename = db.Column(db.String(64), index = False, unique = True) # why is the filename unique?
	label = db.Column(db.String(64), index = False, unique = False)
	date = db.Column(db.DateTime, index = False, unique = False)
	timestamp = db.Column(db.DateTime)
	issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))

class Diagnosis(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	doc_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
	issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
	diagnosis = db.Column(db.String(512), unique=False)




