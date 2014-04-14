from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('isCertified', Boolean),
    Column('isAvailable', Boolean),
    Column('hospital', String),
    Column('city', String),
    Column('state', String),
    Column('country', String),
    Column('user_id', Integer),
)

patient = Table('patient', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstName', String(length=120)),
    Column('lastName', String(length=120)),
    Column('gender', String(length=12)),
    Column('age', Integer),
    Column('city', String(length=120)),
    Column('state', String(length=120)),
    Column('zipcode', Integer),
    Column('country', String(length=120)),
    Column('phone', Integer),
    Column('ethnicity', String(length=120)),
    Column('user_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('password', String),
    Column('email', String),
    Column('isDoctor', Boolean),
    Column('firstName', String),
    Column('lastName', String),
    Column('gender', String),
    Column('age', Integer),
    Column('city', String),
    Column('state', String),
    Column('zipcode', Integer),
    Column('country', String),
    Column('ethnicity', String),
    Column('timestamp', DateTime),
)

doctor = Table('doctor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstName', String(length=120)),
    Column('lastName', String(length=120)),
    Column('gender', String(length=12)),
    Column('age', Integer),
    Column('city', String(length=120)),
    Column('state', String(length=120)),
    Column('zipcode', Integer),
    Column('country', String(length=120)),
    Column('phone', Integer),
    Column('medicalDegree', String(length=120)),
    Column('medicalSchool', String(length=120)),
    Column('degreeYear', Integer),
    Column('isCertified', Boolean),
    Column('hospital', String(length=120)),
    Column('city2', String(length=120)),
    Column('state2', String(length=120)),
    Column('country2', String(length=120)),
    Column('maxNumIssues', Integer),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['patient'].columns['phone'].create()
    pre_meta.tables['user'].columns['age'].drop()
    pre_meta.tables['user'].columns['city'].drop()
    pre_meta.tables['user'].columns['country'].drop()
    pre_meta.tables['user'].columns['ethnicity'].drop()
    pre_meta.tables['user'].columns['firstName'].drop()
    pre_meta.tables['user'].columns['gender'].drop()
    pre_meta.tables['user'].columns['lastName'].drop()
    pre_meta.tables['user'].columns['state'].drop()
    pre_meta.tables['user'].columns['zipcode'].drop()
    post_meta.tables['doctor'].columns['age'].create()
    post_meta.tables['doctor'].columns['city2'].create()
    post_meta.tables['doctor'].columns['country2'].create()
    post_meta.tables['doctor'].columns['degreeYear'].create()
    post_meta.tables['doctor'].columns['firstName'].create()
    post_meta.tables['doctor'].columns['gender'].create()
    post_meta.tables['doctor'].columns['lastName'].create()
    post_meta.tables['doctor'].columns['maxNumIssues'].create()
    post_meta.tables['doctor'].columns['medicalDegree'].create()
    post_meta.tables['doctor'].columns['medicalSchool'].create()
    post_meta.tables['doctor'].columns['phone'].create()
    post_meta.tables['doctor'].columns['state2'].create()
    post_meta.tables['doctor'].columns['zipcode'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['patient'].columns['phone'].drop()
    pre_meta.tables['user'].columns['age'].create()
    pre_meta.tables['user'].columns['city'].create()
    pre_meta.tables['user'].columns['country'].create()
    pre_meta.tables['user'].columns['ethnicity'].create()
    pre_meta.tables['user'].columns['firstName'].create()
    pre_meta.tables['user'].columns['gender'].create()
    pre_meta.tables['user'].columns['lastName'].create()
    pre_meta.tables['user'].columns['state'].create()
    pre_meta.tables['user'].columns['zipcode'].create()
    post_meta.tables['doctor'].columns['age'].drop()
    post_meta.tables['doctor'].columns['city2'].drop()
    post_meta.tables['doctor'].columns['country2'].drop()
    post_meta.tables['doctor'].columns['degreeYear'].drop()
    post_meta.tables['doctor'].columns['firstName'].drop()
    post_meta.tables['doctor'].columns['gender'].drop()
    post_meta.tables['doctor'].columns['lastName'].drop()
    post_meta.tables['doctor'].columns['maxNumIssues'].drop()
    post_meta.tables['doctor'].columns['medicalDegree'].drop()
    post_meta.tables['doctor'].columns['medicalSchool'].drop()
    post_meta.tables['doctor'].columns['phone'].drop()
    post_meta.tables['doctor'].columns['state2'].drop()
    post_meta.tables['doctor'].columns['zipcode'].drop()
