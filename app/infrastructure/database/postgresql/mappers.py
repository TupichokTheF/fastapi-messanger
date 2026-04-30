from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import registry, composite, relationship

from app.domain.user.entities import User, Contact
from app.domain.message.entities import Message, MessageReceiver
from app.domain.message.value_objects import MessageText
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
    Column("spender_id", ForeignKey("users.id"), nullable=False),
    Column("text", String, nullable=False),
    Column("created_at", DateTime, nullable=False)
)

message_receiver = Table(
    "message_receiver",
    metadata,
    Column("message_id", Integer, ForeignKey("messages.id"), primary_key=True, nullable=False),
    Column("receiver_id", Integer, ForeignKey("users.id"), primary_key=True, nullable=False),
    Column("read_at", DateTime, nullable=True)
)

contact_table = Table(
    "contacts",
    metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True, nullable = False),
    Column("contact_id", Integer, ForeignKey("users.id"), primary_key=True, nullable = False),
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
            "_created_at": message_table.c.created_at,
            "_text": composite(MessageText, "col_text"),
        }
    )

    mapper_registry.map_imperatively(
        Contact,
        contact_table,
        properties={
            "_user": relationship(
                User,
                foreign_keys=[contact_table.c.user_id],
                backref="contacts",
                lazy="joined",
            ),
            "_contact": relationship(
                User,
                foreign_keys=[contact_table.c.contact_id],
                backref="contact_of",
                lazy="joined",
            ),
            "_created_at": contact_table.c.created_at,
        },
    )

    mapper_registry.map_imperatively(
        MessageReceiver,
        message_receiver,
        properties={
            "_message": relationship(
                Message,
                foreign_keys=[message_receiver.c.message_id],
                backref="message_receiver",
                lazy="joined",
            ),
            "_receiver": relationship(
                User,
                foreign_keys=[message_receiver.c.receiver_id],
                backref="message_receiver_",
                lazy="joined",
            ),
            "_read_at": message_receiver.c.read_at
        }
    )