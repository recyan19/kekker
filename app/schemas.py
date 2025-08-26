"""Schemas for FastAPI CRUD application."""
from datetime import datetime

from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr


class PostBase(BaseModel):
    """Base model for Post schema."""
    title: Annotated[str, Field(max_length=80)]
    content: Annotated[str, Field(max_length=800)]
    published: bool = True


class PostCreate(PostBase):
    """Schema for creating a new Post."""


class UserOut(BaseModel):
    """Schema for User output."""
    id: int
    email: EmailStr
    # created_at: datetime

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class Post(PostBase):
    """Schema for Post with ID."""
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class PostOut(BaseModel):
    """Schema for Post output with votes count."""
    Post: Post
    votes: int

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class UserCreate(BaseModel):
    """Schema for creating a new User."""
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema for User login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data."""
    user_id: Optional[str] = None


class Vote(BaseModel):
    """Schema for Vote."""
    post_id: Annotated[int, Field(ge=1)]
    dir: Annotated[int, Field(ge=0, le=1)]

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class CommentBase(BaseModel):
    """Base model for Comment schema."""
    content: Annotated[str, Field(max_length=800)]


class CommentCreate(CommentBase):
    """Schema for creating a new Comment."""
    post_id: Annotated[int, Field(ge=1)]


class CommentUpdate(CommentBase):
    """Schema for updating Comment"""


class Comment(CommentBase):
    """Schema for Comment with ID."""
    id: int
    created_at: datetime
    post_id: int
    owner: UserOut

    class Config:
        """Pydantic configuration."""
        from_attributes = True
