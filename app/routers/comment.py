"""CRUD operations for comments in a FastAPI application."""
from typing import List

from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app import models, schemas, oauth2
from app.database import get_db


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[schemas.Comment])
def get_comments(post_id: int, limit: int = 10, skip: int = 0,
                 order: str = "desc",
                 db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):  # pylint: disable=unused-argument
    """ Get comments by Post id"""
    sort_column = getattr(models.Comment, "created_at", models.Comment.created_at)
    sort_order = desc(sort_column) if order.lower() == "desc" else asc(sort_column)

    results = (
        db.query(models.Comment)
        .filter(models.Comment.post_id == post_id)
        .order_by(sort_order)
        .limit(min(limit, 50))
        .offset(skip)
        .all()
    )
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.get_current_user)):
    """ Create a comment for a post """
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {comment.post_id} does not exist"
        )

    new_comment = models.Comment(
        owner_id=current_user.id,
        **comment.model_dump()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.get_current_user)):
    """ Delete a comment by ID """
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    comment = comment_query.first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id: {comment_id} does not exist"
        )

    if comment.owner_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    comment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{comment_id}", response_model=schemas.Comment)
def update_comment(comment_id: int,
                   updated_comment: schemas.CommentUpdate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(oauth2.get_current_user)
                   ):
    """ Update Comment by id """
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    comment = comment_query.first()
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id: {comment_id} was not found"
        )
    if comment.owner_id != current_user.id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    comment_query.update(updated_comment.model_dump(), synchronize_session=False)  # type: ignore
    db.commit()
    return comment_query.first()
