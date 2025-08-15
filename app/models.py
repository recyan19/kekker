"""Database models for the FastAPI CRUD application."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from app.database import Base


class Post(Base):
    """Post model for the database."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(80), nullable=False)
    content = Column(String(800), nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, 
                      ForeignKey("users.id", ondelete="CASCADE"),
                      nullable=False,
                      index=True
                      )

    owner = relationship("User")#, back_populates="posts")


class User(Base):
    """User model for the database."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    phone_number = Column(String, nullable=True)


class Vote(Base):
    """Vote model for the database."""

    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
