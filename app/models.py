from app import db
import time
from datetime import datetime
from sqlalchemy.orm import class_mapper, ColumnProperty



doc_table = db.Table('doc_table',
	db.Column('doc_id', db.Integer, db.ForeignKey('doctor.id')),
	db.Column('issue_id', db.Integer, db.ForeignKey('issue.id'))
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	password = db.Column(db.String(64), index = False, unique = False)
	email = db.Column(db.String(120), index = True, unique = True)
	timestamp = db.Column(db.DateTime, index = False, unique = False, default=datetime.utcnow())
	role = db.Column(db.String(64), index=True, unique=False)
	verified = db.Column(db.Boolean, default=False)
	# Relationships
	patient = db.relationship('Patient', backref='user', uselist=False)
	doctor = db.relationship('Doctor', backref='user', uselist=False)

	def isPatient(self):
		if self.role=='PATIENT':
			return True
		return False

	def isDoctor(self):
		if self.role=='DOCTOR':
			return True
		return False

	def isAdmin(self):
		if self.role=='ADMIN':
			return True
		return False

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
	# Profile information
	first_name = db.Column(db.String(120), index = True, unique = False)
	last_name = db.Column(db.String(120), index = True, unique = False)
	gender = db.Column(db.String(12), index = True, unique = False)
	age = db.Column(db.Integer, index = True, unique = False)
	# Address fields
	city = db.Column(db.String(120), index = True, unique = False)
	state = db.Column(db.String(120), index = True, unique = False)
	zipcode = db.Column(db.Integer, index = True, unique = False)
	country = db.Column(db.String(120), index = True, unique = False)
	phone = db.Column(db.Integer, index=True, unique = False)
	# Others
	ethnicity = db.Column(db.String(120), index = True, unique = False) # Should be optional - legal issues(?) if we force users to reveal this information
	# DermaNet
	is_complete = db.Column(db.Boolean(), index = True, unique=False, default=0) # is profile complete
	# Relationships
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	issues = db.relationship('Issue', backref='patient', lazy='dynamic')

	def owns_issue(self, id):
		issue = Issue.query.get(id)
		if issue.patient == self:
			return True
		else:
			return False

	def isComplete(self):
		patient = self
		if self.first_name is not None:
			if self.last_name is not None:
				if self.age is not None and self.age !='0':
					if self.phone is not None and self.phone !='0':
						if self.gender == 'male' or self.gender == 'female':
							self.is_complete = True
							db.session.commit()
							return True
		self.is_complete = False
		db.session.commit()
		return False

class Doctor(db.Model):
	id = db.Column(db.Integer, primary_key = True)	

	# Profile information
	first_name = db.Column(db.String(120), index = True, unique = False, default="")
	last_name = db.Column('lastName', db.String(120), index = True, unique = False, default="")
	gender = db.Column(db.String(12), index = True, unique = False)
	age = db.Column(db.Integer, index = True, unique = False)
	# Home Address fields
	city = db.Column(db.String(120), index = True, unique = False)
	state = db.Column(db.String(120), index = True, unique = False)
	zipcode = db.Column(db.Integer, index = True, unique = False)
	country = db.Column(db.String(120), index = True, unique = False)
	phone = db.Column(db.Integer, index=True, unique = False)
	# Medical Certification information
	medical_degree = db.Column(db.String(120), index = True, unique = False)
	medical_school = db.Column(db.String(120), index = True, unique = False)
	degree_year = db.Column(db.Integer, index = True, unique = False)
	is_certified = db.Column(db.Boolean, index = True, unique=False, default=0)
	# Hospital Address fields
	hospital_name = db.Column(db.String(120), index = True, unique = False) # which hospital does the doctor practice?
	hospital_city = db.Column(db.String(120), index = True, unique = False)
	hospital_state = db.Column(db.String(120), index = True, unique = False) # or Province
	hospital_country = db.Column(db.String(120), index = True, unique = False)
	# DermaLink stuff
	# maxNumIssues = db.Column(db.Integer, index = True, unique = False, default=1) # Max Number of Issues at a time which doctor can handle
	issue_limit = db.Column(db.Integer(), index=True, unique=False, default=0) # Number of issues they are willing to have at a time
	is_complete = db.Column(db.Boolean(), index = True, unique=False, default=0) # is profile complete
	is_available = db.Column(db.Boolean, index = True, unique=False, default=1)
	rating = db.Column(db.Float, index=True, unique=False)
	# Relationships
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	issues = db.relationship('Issue', secondary=doc_table, backref=db.backref('doctors', lazy='dynamic')) 
	diagnoses = db.relationship('Diagnosis', backref='doctor', lazy='dynamic')

	def isAvailable(self):
		current_issues = self.currentIssues()
		if (current_issues >= self.issue_limit):
			self.is_available = 0
			db.session.commit()
			return False
		elif (current_issues <= self.issue_limit):
			self.is_available = 1
			db.session.commit()
			return True
		else:
			self.is_available = 0
			db.session.commit()
			return False

	# Returns the number of unsolved issues currently assigned to the doctor		
	def currentIssues(self):
		return Issue.query.filter(Issue.doctors.any(id=self.id)).count()

	def owns_issue(self, id):
		doctor_id = self.id
		assigned_issues = Issue.query.filter(Issue.doctors.any(id=doctor_id)).all()
		for issue in assigned_issues:
			if int(issue.id) is int(id):
				return True
		return False

	def isComplete(self):
		if self.first_name is not None and self.last_name is not None:
			if self.hospital_name is not None:
				if self.city is not None and self.state is not None and self.country is not None:
					if self.phone is not None and self.phone !='0':
						if self.issue_limit != '0':
							self.is_complete = True
							db.session.commit()
							return True
		self.is_complete = False
		db.session.commit()
		return False


# Set of images pertaining to a single issue
class Issue(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	# bodyPart = db.Column(db.String(64), index = False, unique = False) 
	summary = db.Column(db.String(250), index = False, unique = False)
	# # Need to keep more information about the issue
	timestamp = db.Column(db.DateTime, index = False, unique = False, default=datetime.utcnow()) # when was the issue created online
	# howOld = db.Column(db.Integer(2), index = False, unique = False) # how many weeks old is the 'issue'
	is_closed = db.Column(db.Boolean, index = False, unique = False, default=False) # has the 'issue' been resolved?
	is_complete = db.Column(db.Boolean, index = False, unique = False, default = False) 
	# Relationships
	patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
	images = db.relationship('Image', backref='issue', lazy='dynamic')
	diagnoses = db.relationship('Diagnosis', backref='issue', lazy='dynamic')

	def isComplete(self):
		for col in self.columns:
			if self.col:
				self.is_complete = False
				return False
		self.is_complete = True
		return True

	def columns(self):
		return [prop.key for prop in class_mapper(self.__class__).iterate_properties
			if isinstance(prop, ColumnProperty)]

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
	timestamp = db.Column(db.DateTime, index = False, unique = False)

class TokenUser(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	token = db.Column(db.String(64), index=True)	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
