from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
issue = Table('issue', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('summary', String),
    Column('user_id', Integer),
    Column('isClosed', Boolean),
    Column('timestamp', DateTime),
)

issue = Table('issue', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('summary', String(length=64)),
    Column('timestamp', DateTime),
    Column('isClosed', Boolean),
    Column('patient_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['issue'].columns['user_id'].drop()
    post_meta.tables['issue'].columns['patient_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['issue'].columns['user_id'].create()
    post_meta.tables['issue'].columns['patient_id'].drop()
