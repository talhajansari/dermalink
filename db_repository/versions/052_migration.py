from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
doctor = Table('doctor', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String),
    Column('last_name', String),
    Column('gender', String),
    Column('age', Integer),
    Column('city', String),
    Column('state', String),
    Column('zipcode', Integer),
    Column('country', String),
    Column('phone', Integer),
    Column('medical_degree', String),
    Column('medical_school', String),
    Column('degree_year', Integer),
    Column('is_certified', Boolean),
    Column('hospital_name', String),
    Column('hospital_city', String),
    Column('hospital_state', String),
    Column('hospital_country', String),
    Column('issue_limit', Integer),
    Column('is_complete', Boolean),
    Column('is_available', Boolean),
    Column('rating', Float),
    Column('user_id', Integer),
)

doctor = Table('doctor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=120)),
    Column('lastName', String(length=120)),
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
    pre_meta.tables['doctor'].columns['last_name'].drop()
    post_meta.tables['doctor'].columns['lastName'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['doctor'].columns['last_name'].create()
    post_meta.tables['doctor'].columns['lastName'].drop()
