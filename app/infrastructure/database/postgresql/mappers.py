from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import registry, composite

from app.domain.user.entities import User
from app.domain.user.value_objects import UserEmail, UserPassword, UserUsername

mapper_registry = registry()
metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True),
    Column("password", String(255)),
    Column("email", String(255), unique=True),
)

def init_tables():
    if User not in mapper_registry.mappers:
        mapper_registry.map_imperatively(
            User,
            user_table,
            properties={
                "_username_col": user_table.c.username,
                "_email_col": user_table.c.email,
                "_password_col": user_table.c.password,

                "username": composite(UserUsername, "_username_col"),
                "email": composite(UserEmail, "_email_col"),
                "password": composite(UserPassword, "_password_col"),
            }
        )