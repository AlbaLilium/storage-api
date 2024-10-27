from itertools import product

from fastapi import HTTPException
from sqlalchemy import select, delete

from app.controllers.crud.base_queries import BaseOperation
from app.data.models.order_model import OrderItem, Order
from app.data.models.product_model import Product
from app.data.serializers.order_item_serializer import OrderItemBase


class OrderItemOperation(BaseOperation):

    async def create_order_item(
            self, order_id: int, product_id: int, product_amount: int
    ) -> OrderItemBase:

        product_object = await self.session.execute(select(Product).where(Product.id == product_id))
        product = product_object.scalars().first()

        if not product:
            await self.session.execute(delete(Order).where(Order.id == product.id))
            raise HTTPException(status_code=400, detail="Product does not exist")
        if product.amount < product_amount:
            await self.session.execute(delete(Order).where(Order.id == product.id))
            raise HTTPException(status_code=400, detail="Not enough product")

        product.amount -= product_amount
        await self._save_object(product)
        new_order_item_object = OrderItem(
            order_id=order_id, product_id=product_id, product_amount=product_amount
        )

        await self._save_object(new_order_item_object)

        return OrderItemBase.model_validate(new_order_item_object)
