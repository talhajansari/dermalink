import datetime
from flask import url_for
from app import db
from flask.ext.mongoengine.wtf import model_form

# Choices
GENDER = ('male','female','other')
ROLE = ('patient', 'doctor', 'admin')
ETHNICITY = ('asian', 'south asian', 'caucasian',
    'hispanic', 'black', 'arab', 'other')

# class Post(db.Document):
#     created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
#     title = db.StringField(max_length=255, required=True)
#     slug = db.StringField(max_length=255, required=True)
#     body = db.StringField(required=True)
#     comments = db.ListField(db.EmbeddedDocumentField('Comment'))

#     def get_absolute_url(self):
#         return url_for('post', kwargs={"slug": self.slug})

#     def __unicode__(self):
#         return self.title

#     meta = {
#         'allow_inheritance': True,
#         'indexes': ['-created_at', 'slug'],
#         'ordering': ['-created_at']
#     }

class User(db.Document):
    id = db.IntField(primary_key=True, unique=True, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    email = db.EmailField(required=True)
    role = db.StringField(choices=ROLE, required=True, max_length=10)
    # relationships

    meta = {'allow_inheritance'=True}



class Patient(User):
    # profile
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    age = db.IntField(max_length=3)
    gender = db.StringField(choices=GENDER, max_length=10)
    ethnicity = db.StringField()
    # address
    address_line_1 = db.StringField()
    address_line_2 = db.StringField()
    city = db.StringField()
    zipcode = db.StringField()
    state = db.StringField()
    country = db.StringField()
    phone = db.StringField()
    # back_end
    is_complete = db.BooleanField()
    # relationships


class Doctor(User):
    # profile
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    age = db.IntField(max_length=3)
    gender = db.StringField(choices=GENDER, max_length=10)
    ethnicity = db.StringField()
    # qualifications
    medical_degree = db.StringField()
    medical_school = db.StringField()
    # work address
    hospital_name = db.StringField()
    address_line_1 = db.StringField()
    address_line_2 = db.StringField()
    city = db.StringField()
    zipcode = db.IntField(max_length=5)
    state = db.StringField()
    country = db.StringField()
    phone = db.StringField()
    # back_end
    is_complete = db.BooleanField()
    is_verified = db.BooleanField()
    issue_limit = db.IntField(max_length=2)
    rating = db.IntField(max_length=1)
    # relationships 


class Admin(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)

class Issue(db.Document):
    id = db.IntField(primary_key=True, unique=True, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    subject = db.StringField(max_length=255)
    summary = db.StringField()
    is_closed = db.BooleanField(default=False)
    # relationship
    patient = db.ReferenceField(Patient)
    doctors = db.ListField(db.ReferenceField(Doctor))


class Images(db.Document):
    id = db.IntField(primary_key=True, unique=True, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    filename = db.StringField(unique=True, max_length=64)
    original_filename = db.StringField()
    label = db.StringField(max_length=64)
    quality = db.IntField(max_length=1)
    # relationship
    issue = db.ReferenceField(Issue)

class Diagnoses(db.Document):
    id = db.IntField(primary_key=True, unique=True, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    comment = db.StringField()
    # relationship
    doctor = db.ReferenceField(Doctor)
    issue = db.ReferenceField(Issue)

class TokenUser(db.Document):
    id = db.IntField(primary_key=True, unique=True, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    token = db.StringField(max_length=64)
    user_id = db.IntField()


patientProfileForm = model_form(patient) 
