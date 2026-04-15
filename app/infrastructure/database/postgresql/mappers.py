from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import registry

from app.domain.user.entities import User

mapper_registry = registry()
metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("password", String(255)),
    Column("email", String(20)),
)

def init_tables():
    mapper_registry.map_imperatively(User, user_table)