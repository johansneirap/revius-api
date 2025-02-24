from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.security import get_current_user
from ..database import get_db
from ..schemas.review import ReviewCreate, Review, Comment, CommentCreate
from ..models.user import User as UserModel
from ..models.review import (
    Review as ReviewModel,
    Comment as CommentModel,
    Like,
    ReviewImage
)

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)


@router.post("/", response_model=Review)
async def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Crear nueva review"""
    # Verificar si el usuario ya ha revisado este producto
    existing_review = db.query(ReviewModel)\
        .filter(
            ReviewModel.user_id == current_user.id,
            ReviewModel.product_id == review.product_id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this product"
        )

    db_review = ReviewModel(
        **review.dict(exclude={'images'}),
        user_id=current_user.id
    )

    # Manejar imágenes si existen
    if review.images:
        for image_url in review.images:
            db_review.images.append(ReviewImage(image_url=image_url))

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # Actualizar estadísticas del producto
    product = db_review.product
    reviews = db.query(ReviewModel).filter(
        ReviewModel.product_id == product.id).all()
    product.review_count = len(reviews)
    product.average_rating = sum(r.rating for r in reviews) / len(reviews)
    db.commit()

    return db_review


@router.post("/{review_id}/comments", response_model=Comment)
async def create_comment(
    review_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Agregar comentario a una review"""
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db_comment = CommentModel(
        **comment.dict(),
        review_id=review_id,
        user_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.post("/{review_id}/like")
async def like_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Dar like a una review"""
    # Verificar si ya dio like
    existing_like = db.query(Like)\
        .filter(
            Like.user_id == current_user.id,
            Like.review_id == review_id
    ).first()

    if existing_like:
        # Si ya existe el like, lo removemos (unlike)
        db.delete(existing_like)
        db.commit()
        return {"message": "Review unliked successfully"}

    # Si no existe, creamos el like
    like = Like(user_id=current_user.id, review_id=review_id)
    db.add(like)
    db.commit()
    return {"message": "Review liked successfully"}


@router.get("/", response_model=List[Review])
async def read_reviews(
    skip: int = 0,
    limit: int = 20,
    product_id: Optional[int] = None,
    user_id: Optional[int] = None,
    min_rating: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar reviews con filtros opcionales"""
    query = db.query(ReviewModel)

    if product_id:
        query = query.filter(ReviewModel.product_id == product_id)
    if user_id:
        query = query.filter(ReviewModel.user_id == user_id)
    if min_rating:
        query = query.filter(ReviewModel.rating >= min_rating)

    reviews = query.order_by(ReviewModel.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return reviews
