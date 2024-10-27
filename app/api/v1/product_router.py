from fastapi import APIRouter

from app.api.v1.dependecies.general_validator import validate_id
from app.api.v1.dependecies.product_validator import validate_numeric_values
from app.controllers.queries.product_queries import ProductOperation
from app.data.serializers.product_serializer import (
    CreateProductSerializer,
    ListProductSerializer,
    ProductBase,
    UpdateProductSerializer,
)

product_router = APIRouter(prefix="/products", tags=["product"])


@product_router.get(path="/", response_model=ListProductSerializer)
async def get_all_products():
    """
    Get all products in database.

    :return product_list: ListProductSerializer
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

    :param product_id: int
    :raise HTTPException 400 if product_id < 0
    :return product: ProductBase

    """
    async with ProductOperation() as db:
        return await db.get_product(product_id=validate_id(id=product_id))


@product_router.post(path="/")
async def create_new_product(
    new_product: CreateProductSerializer,
):
    """
    Create and save new product in database.

    :param new_product:
        title: str
        description: str
        cost: Decimal
        amount: int

    :raise HTTPException 400 if
        cost < 0,
        amount < 0,
        title is empty,
        description is empty

    :return new_product_id: dict[str: int]
    """
    async with ProductOperation() as db:
        new_product_id = await db.create_product(new_product=new_product)

    return {"id": new_product_id}


@product_router.delete(path="/{id}")
async def delete_product(deleted_product_id: int):
    """
    Delete product in database.

    :params deleted_product_id: int

    :raise HTTPException 400
        if deleted_product_id < 0

    :return response: dict[str:str]
    """
    async with ProductOperation() as db:
        response = await db.delete_product(
            deleted_product_id=validate_id(deleted_product_id)
        )

    return response


@product_router.put(path="/{id}", response_model=ProductBase)
async def update_product_information(
    updated_product: UpdateProductSerializer,
):
    """
    Update product in database.

    :param updated_product:
        id: int
        title: str | None
        description: str | None
        cost: Decimal| None
        amount: int| None

    :raise HTTPException 400
        if
        cost < 0 and
        amount < 0

    :return: product:
        id: int
        title: str
        description: str
        cost: Decimal
        amount: int
    """
    if validate_numeric_values(
        cost=updated_product.cost,
        amount=updated_product.amount,
    ):

        async with ProductOperation() as db:
            refreshed_product = await db.update_product(updated_product)
    return refreshed_product
