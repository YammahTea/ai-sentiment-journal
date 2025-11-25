import uuid
from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy import String, Text, Float, DateTime, ForeignKey, Uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./journal.db"

class Base(DeclarativeBase):
    pass


# class User(SQLAlchemyBaseUserTableUUID, Base):
#   # This creates a link so we can say user.posts to get all their entries
#     posts = relationship("Journal", back_populates="user")

class Journal(Base): # Columns: id, message, sentiment_score, mood, created_at
    __tablename__ = "journal"

  # Message ID
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

  # Message
    message: Mapped[str] = mapped_column(Text, nullable=False)

  # Analyzed message info (sentiment score and mood)
    sentiment_score: Mapped[float] = mapped_column(Float, nullable=False)
    mood: Mapped[str] = mapped_column(String, nullable=False)

  # Message time
    created_at: Mapped[datetime] = mapped_column(DateTime, default= lambda : datetime.now(timezone.utc))

  # Owner of message
  #   user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("user_id"))\

  # Relationship back to User
  #   user = relationship("User", back_populates="posts")


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
      yield session

#
# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#    yield SQLAlchemyUserDatabase(session, User)
