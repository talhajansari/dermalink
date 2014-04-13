from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
derm_table = Table('derm_table', post_meta,
    Column('dermatologist_id', Integer),
    Column('issue_id', Integer),
)

doc_table = Table('doc_table', post_meta,
    Column('doc_id', Integer),
    Column('issue_id', Integer),
)

doctor = Table('doctor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('isCertified', Boolean),
    Column('hospital', String(length=120)),
    Column('city', String(length=120)),
    Column('state', String(length=120)),
    Column('country', String(length=120)),
    Column('user_id', Integer),
)

patient = Table('patient', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
)

issue = Table('issue', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('summary', String),
    Column('user_id', Integer),
    Column('dermatologist_id', Integer),
    Column('isClosed', Boolean),
    Column('timestamp', DateTime),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('password', String(length=64)),
    Column('email', String(length=120)),
    Column('isDoctor', Boolean),
    Column('firstName', String(length=120)),
    Column('lastName', String(length=120)),
    Column('gender', String(length=12)),
    Column('age', Integer),
    Column('city', String(length=120)),
    Column('state', String(length=120)),
    Column('zipcode', Integer),
    Column('country', String(length=120)),
    Column('ethnicity', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['derm_table'].create()
    post_meta.tables['doc_table'].create()
    post_meta.tables['doctor'].create()
    post_meta.tables['patient'].create()
    pre_meta.tables['issue'].columns['dermatologist_id'].drop()
    post_meta.tables['user'].columns['isDoctor'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['derm_table'].drop()
    post_meta.tables['doc_table'].drop()
    post_meta.tables['doctor'].drop()
    post_meta.tables['patient'].drop()
    pre_meta.tables['issue'].columns['dermatologist_id'].create()
    post_meta.tables['user'].columns['isDoctor'].drop()
