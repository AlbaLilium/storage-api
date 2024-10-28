from fastapi import HTTPException
from sqlalchemy import delete, select, update

from app.controllers.queries.base import BaseOperation
from app.data.models.product import Product as ProductModel
from app.data.serializers.product import (CreateProductSerializer,
                                          ListProductSerializer, ProductBase,
                                          UpdateProductSerializer)


class ProductOperation(BaseOperation):

    async def get_all_products(self) -> ListProductSerializer:
        query = await self.session.execute(select(ProductModel))
        products = query.scalars().all()
        return ListProductSerializer(product_list=products)

    async def get_product(self, product_id: int) -> ProductBase:
        query = await self.session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = query.scalars().first()

        if not product:
            raise HTTPException(status_code=400, detail="Product does not exist")

        return ProductBase.model_validate(product)

    async def delete_product(self, deleted_product_id: int) -> dict[str:str]:
        await self.get_product(product_id=deleted_product_id)
        await self.session.execute(
            delete(ProductModel).where(ProductModel.id == deleted_product_id)
        )
        return {"success": "product removed"}

    async def create_product(self, new_product: CreateProductSerializer) -> int:
        product_object = ProductModel(
            title=new_product.title,
            description=new_product.description,
            cost=new_product.cost,
            amount=new_product.amount,
        )

        await self._save_object(product_object)

        return product_object.id

    async def update_product(
        self, product_update: UpdateProductSerializer
    ) -> ProductBase:
        query = await self.session.execute(
            select(ProductModel).where(ProductModel.id == product_update.id)
        )
        product = query.scalars().first()

        if not product:
            raise HTTPException(status_code=400, detail="Product does not exist")

        if product_update.amount:
            product.amount = product_update.amount
        elif product_update.cost:
            product.cost = product_update.cost
        elif product_update.title:
            product.title = product_update.title
        elif product_update.description:
            product.description = product_update.description

        await self._save_object(product)

        return ProductBase(
            id=product.id,
            amount=product.amount,
            cost=product.cost,
            description=product.description,
            title=product.title,
        )
