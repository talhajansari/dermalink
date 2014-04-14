from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
issue = Table('issue', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('summary', String(length=250)),
    Column('timestamp', DateTime, default=ColumnDefault(datetime.datetime(2014, 4, 14, 8, 12, 57, 788677))),
    Column('isClosed', Boolean),
    Column('isComplete', Boolean, default=ColumnDefault(False)),
    Column('patient_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['issue'].columns['isComplete'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['issue'].columns['isComplete'].drop()
