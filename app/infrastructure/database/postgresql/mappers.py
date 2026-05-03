from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Enum
from sqlalchemy.orm import registry, composite, relationship

from app.domain.user import User, UserEmail, UserPassword, UserUsername
from app.domain.message import Message, MessageText
from app.domain.chat import Chat, ChatMember, ChatName, ChatType


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

chat_table = Table(
    "chats",
    metadata,
    Column("chat_id", Integer, primary_key=True),
    Column("name", String(50), nullable = False),
    Column(
        "type",
        Enum(
            ChatType,
            name="chat_type",
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
    ),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

chat_member = Table(
    "chat_member",
    metadata,
    Column("chat_id", Integer, ForeignKey("chats.chat_id"), primary_key = True, nullable=False),
    Column("member_id", Integer, ForeignKey("users.id"), primary_key=True, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

message_table = Table(
    "messages",
    metadata,
    Column('id', Integer, primary_key=True),
    Column("chat_id", Integer, ForeignKey("chats.chat_id"), nullable=False),
    Column("spender_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("text", String, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)


TABLES = []


def table_initializer(func):
    TABLES.append(func)
    return func


@table_initializer
def init_user_tables():
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


@table_initializer
def init_chat_tables():
    mapper_registry.map_imperatively(
        Chat,
        chat_table,
        properties={
            "col_name": chat_table.c.name,
            "_type": chat_table.c.type,
            "_name": composite(ChatName, "col_name"),
            "_members": relationship(ChatMember, back_populates="_chat", lazy="selectin", collection_class=set),
            "_created_at": chat_table.c.created_at
        }
    )

    mapper_registry.map_imperatively(
        ChatMember,
        chat_member,
        properties={
            "_chat": relationship(Chat, back_populates="_members", lazy="joined"),
            "_member": relationship(User, lazy="joined"),
            "_created_at": chat_member.c.created_at,
        }
    )


@table_initializer
def init_message_tables():
    mapper_registry.map_imperatively(
        Message,
        message_table,
        properties={
            "col_text": message_table.c.text,
            "_chat": relationship(Chat, lazy="joined"),
            "_spender": relationship(User, lazy="joined"),
            "_created_at": message_table.c.created_at,
            "_text": composite(MessageText, "col_text"),
        }
    )


def init_tables():
    for func in TABLES:
        func()