from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import registry, composite, relationship

from app.domain.user.entities import User
from app.domain.message.entities import Message
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

message_table = Table(
    "messages",
    metadata,
    Column('id', Integer, primary_key=True),
    Column("spender", ForeignKey("users.id"), nullable=False),
    Column("text", String, nullable=False),
    Column("created_at", DateTime, nullable=False)
)

def init_tables():
    mapper_registry.map_imperatively(
        User,
        user_table,
        properties={
            "_col_username": user_table.c.username,
            "_col_email": user_table.c.email,
            "_col_password": user_table.c.password,

            "_username": composite(UserUsername, "_col_username"),
            "_email": composite(UserEmail, "_col_email"),
            "_password": composite(UserPassword, "_col_password"),
        }
    )

    mapper_registry.map_imperatively(
        Message,
        message_table,
        properties={
            "col_text": message_table.c.text,
            "_spender": relationship(User, backref="messages", lazy="joined"),
            "created_at": message_table.c.created_at
        }
    )