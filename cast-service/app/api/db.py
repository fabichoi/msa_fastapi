import os

from databases import Database
from sqlalchemy import Column, MetaData, Table, String, Integer, create_engine

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

casts = Table(
    'casts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('nationality', String(20)),
)

database = Database(DATABASE_URI)
