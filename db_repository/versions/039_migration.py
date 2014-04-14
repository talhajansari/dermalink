from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
patient = Table('patient', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('city', String(length=120)),
    Column('state', String(length=120)),
    Column('zipcode', Integer),
    Column('country', String(length=120)),
    Column('phone', Integer),
    Column('user_id', Integer),
    Column('isComplete', Boolean),
    Column('firstName', String(length=120)),
    Column('lastName', String(length=120)),
    Column('gender', String(length=12)),
    Column('age', Integer),
    Column('ethnicity', String(length=120)),
)

doctor = Table('doctor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('firstName', String(length=120)),
    Column('lastName', String(length=120)),
    Column('gender', String(length=12)),
    Column('age', Integer),
    Column('isComplete', Boolean),
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
    Column('maxNumIssues', Integer, default=ColumnDefault(1)),
    Column('isAvailable', Boolean, default=ColumnDefault(1)),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['patient'].columns['isComplete'].create()
    post_meta.tables['doctor'].columns['isComplete'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['patient'].columns['isComplete'].drop()
    post_meta.tables['doctor'].columns['isComplete'].drop()
