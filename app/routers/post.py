"""CRUD operations for posts in a FastAPI application."""
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas, oauth2
from app.database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: models.User = Depends(oauth2.get_current_user),  # pylint: disable=unused-argument
              limit: int = 10,
              skip:int = 0,
              search: Optional[str] = ""
              ):
    """ Get posts """
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes")) # pylint: disable=not-callable
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip).all()
      )
    return results


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int,
             db: Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)  # pylint: disable=unused-argument
             ):
    """ Get post by ID """
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes")) # pylint: disable=not-callable
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == post_id)
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found"
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)
                ):
    """ Create post """
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Refresh to get the new post with ID
    return new_post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int,
                updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)
                ):
    """ Update post by id """
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found"
        )
    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    post_query.update(updated_post.model_dump(), synchronize_session=False) # type: ignore
    db.commit()
    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)
                ):
    """ Delete post by ID """
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {post_id} was not found"
        )
    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
