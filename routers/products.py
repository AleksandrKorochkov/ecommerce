from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from schemas import CreateProduct
from backend.db_depends import get_db
from sqlalchemy import Insert, select, update
from slugify import slugify
from models.products import Product, Category
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_user

router = APIRouter(prefix='/products', tags=['products'])

# OK!
@router.get('/')
async def all_products(db: Annotated[AsyncSession, Depends(get_db)]):
    product = await db.scalars(select(Product).where(Product.is_active == True, Product.stock > 0))

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No list product is activ!')
    return product.all()


# ok!
@router.post('/create')
async def create_product(db: Annotated[AsyncSession, Depends(get_db)], create_product: CreateProduct, 
                         get_user: Annotated[dict, Depends(get_current_user)]):
    product = await db.scalar(select(Category).where(Category.id == create_product.category))
    if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Такой каттегории нет в базе!"
            )
    if get_user.get('is_admin') or get_user.get('is_supplier'):
        await db.execute(Insert(Product).values(name=create_product.name,
                                        description=create_product.description,
                                        price=create_product.price,
                                        image_url=create_product.image_url,
                                        stock=create_product.stock,
                                        category_id=create_product.category,
                                        supplier_id=get_user.get('id'),
                                        rating=0.0,
                                        slug=slugify(create_product.name)))

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

# Ok
@router.get('/{category_slug}')
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)] ,category_slug: str):
    category = await db.scalar(select(Category).where(Category.slug == category_slug))
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Not found category!!')
    
    subcategory = await db.scalars(select(Category).where(Category.parent_id == category.id))
    category_and_subcategory = [category.id] + [i.id for i in subcategory.all()]
    products_category = await db.scalars(select(Product).where(Product.category_id.in_(category_and_subcategory), Product.is_active == True,
                                                               Product.stock > 0))

    return products_category.all()

# OK!
@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):

    product = await db.scalar(
        select(Product).where(Product.slug == product_slug, Product.is_active == True, Product.stock > 0))

    if product is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    return product

@router.put('/detail/{product_slug}')
async def update_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str,
                         update_product_model: CreateProduct, get_user: Annotated[dict, Depends(get_current_user)]):
    product_update = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    category = await db.scalar(select(Category).where(Category.id == update_product_model.category))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    
    if get_user.get('is_supplier') or get_user.get('is_admin'):
        if get_user.get('id') == product_update.supplier_id or get_user.get('is_admin'):
            await db.execute(
                        update(Product).where(Product.slug == product_slug)
                        .values(name=update_product_model.name,
                                description=update_product_model.description,
                                price=update_product_model.price,
                                image_url=update_product_model.image_url,
                                stock=update_product_model.stock,
                                category_id=update_product_model.category,
                                slug=slugify(update_product_model.name)))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Product update is successful'
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )

@router.delete('/delete')
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str, 
                         get_user: Annotated[dict, Depends(get_current_user)]):
    
    product_delete = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product_delete is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no product found'
            )
    if get_user.get('is_supplier') or get_user.get('is_admin'):
        if get_user.get('is_admin') or (get_user.get('is_supplier') and get_user.get('id') == product_delete.supplier_id):
        # product_delete = await db.scalar(select(Product).where(Product.slug == product_slug))
        
            await db.execute(update(Product).where(Product.slug == product_slug).values(is_active=False))
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Product delete is successful'
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='You are not authorized to use this method'
            )
        
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method"
            )