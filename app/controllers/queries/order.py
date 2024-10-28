from fastapi import HTTPException
from sqlalchemy import delete, select

from app.controllers.queries.base import BaseOperation
from app.data.models.order import Order, OrderItem
from app.data.models.product import Product
from app.data.serializers.order import (ListOrdersSerializer, OrderBase,
                                        OrderCreateSerializer, OrderItemBase,
                                        OrderUpdateStatusSerializer)


class OrderOperation(BaseOperation):

    async def create_order(self, new_order: OrderCreateSerializer) -> int:
        new_order_object = Order(
            status=new_order.status, creation_date=new_order.creation_date
        )
        await self._save_object(new_order_object)

        return new_order_object.id

    async def get_order(self, order_id: int) -> OrderBase:
        query = await self.session.execute(select(Order).where(Order.id == order_id))
        order = query.scalars().first()
        return OrderBase.model_validate(order)

    async def get_all_orders(self) -> ListOrdersSerializer:
        query = await self.session.execute(select(Order))
        orders = query.scalars().all()
        return ListOrdersSerializer(order_list=orders)

    async def update_status(self, new_status: OrderUpdateStatusSerializer) -> OrderBase:
        query = await self.session.execute(
            select(Order).where(Order.id == new_status.id)
        )
        order = query.scalars().first()

        if not order:
            raise HTTPException(status_code=400, detail="Order does not exist")
        order.status = new_status.status

        await self._save_object(order)

        return OrderBase.model_validate(order)


class OrderItemOperation(BaseOperation):

    async def create_order_item(
        self, order_id: int, product_id: int, product_amount: int
    ) -> OrderItemBase:

        product_object = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
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
