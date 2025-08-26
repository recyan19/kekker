"""Main FastAPI application for CRUD operations with PostgreSQL."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app import models
# from app.database import engine
from app.routers import auth, post, user, vote, comment


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(comment.router)

@app.get("/")
def root():
    """Return Home"""
    return {"message": "Welcome to my API!"}
