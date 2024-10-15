from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from schemas import CreateRaitings, CreateReviews
from backend.db_depends import get_db
from sqlalchemy import Insert, select, update
from models.products import Product
from models import *
from sqlalchemy.ext.asyncio import AsyncSession, session
from routers.auth import get_current_user
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/rating_reviews", tags=["rating_reviews"])


@router.get("/")
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    product = await db.scalars(select(Product))
    

    rat_rev = await db.scalars(select(Raview).where(Raview.is_active == True))

    if rat_rev is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No list!')
    
    # query = await db.scalar(select(Raview).options(joinedload(Raview.raiting)))
    result = await db.scalars(select(Raiting).options(joinedload(Raiting.reviews)))

    return (((i.reviews.comment if i.reviews else None), 
             (i.grade if i.grade else None)) 
            for i in result.all())

@router.post('/create')
async def add_review(db: Annotated[AsyncSession, Depends(get_db)], create_review: CreateReviews, 
                               create_rating: CreateRaitings, product_slug: str, get_user: Annotated[dict, Depends(get_current_user)]):


    products = await db.scalar(select(Product).where(Product.slug == product_slug))

    if product_slug is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found product!"
        )
    
    if get_user.get('is_customer') == True:

        rating = Raiting(grade=create_rating.grade, product_id=products.id, user_id=get_user.get("id"))
        db.add(rating)
        await db.commit()

        review = Raview(product_id=products.id, user_id=get_user.get("id"), comment=create_review.comment, 
                        rating_id=rating.id)
        
        db.add(review)
        await db.commit()

        rating_product = await db.scalars(select(Raiting).where(Raiting.product_id == products.id), Raiting.is_active == True)
        
        def count_rating(rating: Raiting) -> float:
            count = 0
            total = 0
            for i in rating_product.all():
                count += 1
                total += i.grade

            return  float(total / count)

        await db.execute(update(Product).where(Product.slug == product_slug).values(rating=count_rating(rating_product)))
        await db.commit()

        return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Successful'
            }
    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )
    
@router.get("/detail/{slag_product}")
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)], slag_product: str):
    product = await db.scalar(select(Product).where(Product.slug == slag_product))

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found product!"
        )
    
    # query = select(Raiting).where(Raiting.product_id == product.id).join(Raview, Raview.rating_id == Raiting.id, isouter=True)
    query = select(Raview).where(Raview.product_id == product.id).options(joinedload(Raview.raiting)) 
    result = await db.execute(query)
    reviews = result.scalars().all()

    # a = [i.raiting.grade if i.raiting else None for i in reviews]
    # b = [i.comment for i in reviews]
    # res = zip(b, a)
    # return res


    return product.name, (((i.comment if i else None),
                           i.raiting.grade if i.raiting else None)
                            for i in reviews)

    # reviews_with_ratings = await db.execute(select(rewiew))

    # rewiew = await db.scalars(select(Raview).where(Raview.product_id == product.id))

    # for review in reviews_with_ratings.all():
    #     print(f"Review: {review.comment}, Rating: {review.raiting.grade}")

@router.delete('/delete')
async def delete_reviews(db: Annotated[AsyncSession, Depends(get_db)],
                         get_use: Annotated[dict, Depends(get_current_user)], rewiews_id: int, product_id: int):
        
    review = await db.scalar(select(Raview).where(Raview.id == rewiews_id))

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product"
        )
        
    if get_use.get('is_admin') == True:

        rat_rev = await db.scalar(select(Raview).where(Raview.id == rewiews_id).options(joinedload(Raview.raiting)))
        
        await db.execute(update(Raview).where(Raview.id == rat_rev.id).values(is_active = False))
        await db.execute(update(Raiting).where(Raiting.id == rat_rev.raiting.id).values(is_active = False))
        await db.commit()

        rating_product = await db.scalars(select(Raiting).where(Raiting.product_id == product_id, Raiting.is_active == True))
        
        def count_rating(rating: Raiting) -> float:
            count = 0
            total = 0
            for i in rating_product.all():
                count += 1
                total += i.grade

            return  float(total / count)
        
        await db.execute(update(Product).where(Product.id == product_id).values(rating=count_rating(rating_product)))
        await db.commit()

    
        return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Raview and Rating delete is successful'}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method"
            )
    
