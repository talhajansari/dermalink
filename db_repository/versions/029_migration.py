from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dermatologists = Table('dermatologists', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('password', String),
    Column('email', String),
    Column('firstName', String),
    Column('lastName', String),
    Column('gender', String),
    Column('age', Integer),
    Column('hospital', String),
    Column('city', String),
    Column('state', String),
    Column('zipcode', Integer),
    Column('country', String),
)

dermatologist = Table('dermatologist', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('password', String(length=64)),
    Column('email', String(length=120)),
    Column('firstName', String(length=120)),
    Column('lastName', String(length=120)),
    Column('gender', String(length=12)),
    Column('age', Integer),
    Column('isCertified', Boolean),
    Column('hospital', String(length=120)),
    Column('city', String(length=120)),
    Column('state', String(length=120)),
    Column('country', String(length=120)),
)

issue = Table('issue', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('summary', String(length=64)),
    Column('user_id', Integer),
    Column('timestamp', DateTime),
    Column('isClosed', Boolean),
    Column('dermatologist_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dermatologists'].drop()
    post_meta.tables['dermatologist'].create()
    post_meta.tables['issue'].columns['dermatologist_id'].create()
    post_meta.tables['issue'].columns['isClosed'].create()
    post_meta.tables['issue'].columns['timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dermatologists'].create()
    post_meta.tables['dermatologist'].drop()
    post_meta.tables['issue'].columns['dermatologist_id'].drop()
    post_meta.tables['issue'].columns['isClosed'].drop()
    post_meta.tables['issue'].columns['timestamp'].drop()
