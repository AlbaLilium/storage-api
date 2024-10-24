from fastapi import APIRouter

from app.controllers.queries.product_queries import ProductOperation
from app.data.serializers.product_serializer import (CreateProductSerializer,
                                                     ListProductSerializer,
                                                     ProductBase,
                                                     UpdateProductSerializer)

product_router = APIRouter(prefix="/products")


@product_router.get(path="/", response_model=ListProductSerializer)
async def get_all_products():
    """
    Get all products in database.

    Returns
    -------
    task_list: ListProductSerializer
    """

    async with ProductOperation() as db:
        product_list = await db.get_all_products()
    return product_list


@product_router.get(path="/{id}", response_model=ProductBase)
async def get_product(
    product_id: int,
):
    """
    Get product in database.

    Parameters
    ----------
    requested_product: ProductSerializer

    Returns
    -------
    product: ProductBase
    """
    async with ProductOperation() as db:
        return await db.get_product(product_id=product_id)


@product_router.post(path="/")
async def create_new_product(
    new_product: CreateProductSerializer,
):
    """

    Parameters
    ----------
    new_product: CreateProductSerializer

    Returns
    -------
    new_product_id: dict[str: str]

    """
    async with ProductOperation() as db:
        new_product_id = await db.create_product(new_product=new_product)

    return {"id": new_product_id}


@product_router.delete(path="/{id}")
async def delete_product(deleted_product_id: int):
    """
    Delete product in database.

    Parameters
    ----------
    deleted_product: ProductSerializer

    Returns
    -------
    response: dict[str:str]
    """
    async with ProductOperation() as db:
        response = await db.delete_product(deleted_product_id=deleted_product_id)

    return response


@product_router.put(path="/{id}", response_model=ProductBase)
async def update_product_information(
    updated_product: UpdateProductSerializer,
):
    """
    Get product in database.

    Parameters
    ----------
    updated_product: UpdateProductSerializer)

    Returns
    -------
    refreshed_product: ProductBase
    """
    async with ProductOperation() as db:
        refreshed_product = await db.update_product(updated_product)
    return refreshed_product
