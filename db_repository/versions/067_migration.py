from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
image = Table('image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('filename', String(length=64)),
    Column('original_filename', String(length=64)),
    Column('label', String(length=64)),
    Column('date', DateTime),
    Column('timestamp', DateTime, default=ColumnDefault(datetime.datetime(2014, 5, 7, 5, 36, 36, 745724))),
    Column('issue_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['image'].columns['original_filename'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['image'].columns['original_filename'].drop()
