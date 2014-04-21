from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
issue = Table('issue', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('summary', String),
    Column('timestamp', DateTime),
    Column('isClosed', Boolean),
    Column('isComplete', Boolean),
    Column('patient_id', Integer),
)

issue = Table('issue', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('summary', String(length=250)),
    Column('timestamp', DateTime, default=ColumnDefault(datetime.datetime(2014, 4, 20, 23, 18, 24, 637785))),
    Column('is_closed', Boolean, default=ColumnDefault(False)),
    Column('is_complete', Boolean, default=ColumnDefault(False)),
    Column('patient_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['issue'].columns['isClosed'].drop()
    pre_meta.tables['issue'].columns['isComplete'].drop()
    post_meta.tables['issue'].columns['is_closed'].create()
    post_meta.tables['issue'].columns['is_complete'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['issue'].columns['isClosed'].create()
    pre_meta.tables['issue'].columns['isComplete'].create()
    post_meta.tables['issue'].columns['is_closed'].drop()
    post_meta.tables['issue'].columns['is_complete'].drop()
