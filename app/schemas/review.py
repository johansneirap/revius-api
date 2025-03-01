from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    review_id: int


class Comment(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ReviewImageBase(BaseModel):
    image_url: str


class ReviewImage(ReviewImageBase):
    id: int
    review_id: int
    model_config = ConfigDict(from_attributes=True)


class ReviewBase(BaseModel):
    title: str
    content: str
    rating: int


class ReviewCreate(ReviewBase):
    product_id: int
    images: Optional[List[str]] = None


class Review(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    images: List[ReviewImage]
    comments: List[Comment]
    like_count: int = 0
    model_config = ConfigDict(from_attributes=True)
