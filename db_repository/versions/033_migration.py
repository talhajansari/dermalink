from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
doctor = Table('doctor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('isCertified', Boolean),
    Column('isAvailable', Boolean),
    Column('hospital', String(length=120)),
    Column('city', String(length=120)),
    Column('state', String(length=120)),
    Column('country', String(length=120)),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['doctor'].columns['isAvailable'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['doctor'].columns['isAvailable'].drop()
