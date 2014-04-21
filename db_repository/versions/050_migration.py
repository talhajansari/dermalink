from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
patient = Table('patient', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstName', String),
    Column('lastName', String),
    Column('gender', String),
    Column('age', Integer),
    Column('city', String),
    Column('state', String),
    Column('zipcode', Integer),
    Column('country', String),
    Column('phone', Integer),
    Column('ethnicity', String),
    Column('user_id', Integer),
)

patient = Table('patient', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=120)),
    Column('last_name', String(length=120)),
    Column('gender', String(length=12)),
    Column('age', Integer),
    Column('city', String(length=120)),
    Column('state', String(length=120)),
    Column('zipcode', Integer),
    Column('country', String(length=120)),
    Column('phone', Integer),
    Column('ethnicity', String(length=120)),
    Column('is_complete', Boolean, default=ColumnDefault(0)),
    Column('user_id', Integer),
)

doctor = Table('doctor', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('lastName', String),
    Column('gender', String),
    Column('age', Integer),
    Column('city', String),
    Column('state', String),
    Column('zipcode', Integer),
    Column('country', String),
    Column('phone', Integer),
    Column('medicalDegree', String),
    Column('medicalSchool', String),
    Column('degreeYear', Integer),
    Column('isCertified', Boolean),
    Column('hospital', String),
    Column('city2', String),
    Column('state2', String),
    Column('country2', String),
    Column('issueLimit', Integer),
    Column('user_id', Integer),
    Column('rating', Float),
    Column('First Name', String),
)

doctor = Table('doctor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=120)),
    Column('last_name', String(length=120)),
    Column('gender', String(length=12)),
    Column('age', Integer),
    Column('city', String(length=120)),
    Column('state', String(length=120)),
    Column('zipcode', Integer),
    Column('country', String(length=120)),
    Column('phone', Integer),
    Column('medical_degree', String(length=120)),
    Column('medical_school', String(length=120)),
    Column('degree_year', Integer),
    Column('is_certified', Boolean, default=ColumnDefault(0)),
    Column('hospital_name', String(length=120)),
    Column('hospital_city', String(length=120)),
    Column('hospital_state', String(length=120)),
    Column('hospital_country', String(length=120)),
    Column('issue_limit', Integer, default=ColumnDefault(0)),
    Column('is_complete', Boolean, default=ColumnDefault(0)),
    Column('is_available', Boolean, default=ColumnDefault(1)),
    Column('rating', Float),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['patient'].columns['firstName'].drop()
    pre_meta.tables['patient'].columns['lastName'].drop()
    post_meta.tables['patient'].columns['first_name'].create()
    post_meta.tables['patient'].columns['is_complete'].create()
    post_meta.tables['patient'].columns['last_name'].create()
    pre_meta.tables['doctor'].columns['First Name'].drop()
    pre_meta.tables['doctor'].columns['city2'].drop()
    pre_meta.tables['doctor'].columns['country2'].drop()
    pre_meta.tables['doctor'].columns['degreeYear'].drop()
    pre_meta.tables['doctor'].columns['hospital'].drop()
    pre_meta.tables['doctor'].columns['isCertified'].drop()
    pre_meta.tables['doctor'].columns['issueLimit'].drop()
    pre_meta.tables['doctor'].columns['lastName'].drop()
    pre_meta.tables['doctor'].columns['medicalDegree'].drop()
    pre_meta.tables['doctor'].columns['medicalSchool'].drop()
    pre_meta.tables['doctor'].columns['state2'].drop()
    post_meta.tables['doctor'].columns['degree_year'].create()
    post_meta.tables['doctor'].columns['first_name'].create()
    post_meta.tables['doctor'].columns['hospital_city'].create()
    post_meta.tables['doctor'].columns['hospital_country'].create()
    post_meta.tables['doctor'].columns['hospital_name'].create()
    post_meta.tables['doctor'].columns['hospital_state'].create()
    post_meta.tables['doctor'].columns['is_available'].create()
    post_meta.tables['doctor'].columns['is_certified'].create()
    post_meta.tables['doctor'].columns['is_complete'].create()
    post_meta.tables['doctor'].columns['issue_limit'].create()
    post_meta.tables['doctor'].columns['last_name'].create()
    post_meta.tables['doctor'].columns['medical_degree'].create()
    post_meta.tables['doctor'].columns['medical_school'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['patient'].columns['firstName'].create()
    pre_meta.tables['patient'].columns['lastName'].create()
    post_meta.tables['patient'].columns['first_name'].drop()
    post_meta.tables['patient'].columns['is_complete'].drop()
    post_meta.tables['patient'].columns['last_name'].drop()
    pre_meta.tables['doctor'].columns['First Name'].create()
    pre_meta.tables['doctor'].columns['city2'].create()
    pre_meta.tables['doctor'].columns['country2'].create()
    pre_meta.tables['doctor'].columns['degreeYear'].create()
    pre_meta.tables['doctor'].columns['hospital'].create()
    pre_meta.tables['doctor'].columns['isCertified'].create()
    pre_meta.tables['doctor'].columns['issueLimit'].create()
    pre_meta.tables['doctor'].columns['lastName'].create()
    pre_meta.tables['doctor'].columns['medicalDegree'].create()
    pre_meta.tables['doctor'].columns['medicalSchool'].create()
    pre_meta.tables['doctor'].columns['state2'].create()
    post_meta.tables['doctor'].columns['degree_year'].drop()
    post_meta.tables['doctor'].columns['first_name'].drop()
    post_meta.tables['doctor'].columns['hospital_city'].drop()
    post_meta.tables['doctor'].columns['hospital_country'].drop()
    post_meta.tables['doctor'].columns['hospital_name'].drop()
    post_meta.tables['doctor'].columns['hospital_state'].drop()
    post_meta.tables['doctor'].columns['is_available'].drop()
    post_meta.tables['doctor'].columns['is_certified'].drop()
    post_meta.tables['doctor'].columns['is_complete'].drop()
    post_meta.tables['doctor'].columns['issue_limit'].drop()
    post_meta.tables['doctor'].columns['last_name'].drop()
    post_meta.tables['doctor'].columns['medical_degree'].drop()
    post_meta.tables['doctor'].columns['medical_school'].drop()
