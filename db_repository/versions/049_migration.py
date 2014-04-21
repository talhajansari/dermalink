from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
doctor = Table('doctor', pre_meta,
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
)

doctor = Table('doctor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('First Name', String(length=120)),
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
    Column('isCertified', Boolean, default=ColumnDefault(0)),
    Column('hospital', String(length=120)),
    Column('city2', String(length=120)),
    Column('state2', String(length=120)),
    Column('country2', String(length=120)),
    Column('issueLimit', Integer, default=ColumnDefault(0)),
    Column('rating', Float),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['doctor'].columns['firstName'].drop()
    post_meta.tables['doctor'].columns['First Name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['doctor'].columns['firstName'].create()
    post_meta.tables['doctor'].columns['First Name'].drop()
