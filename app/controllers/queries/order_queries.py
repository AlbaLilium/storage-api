from fastapi import HTTPException
from sqlalchemy import select

from app.controllers.queries.base_queries import BaseOperation
from app.data.models.order_model import Order
from app.data.serializers.order_serializer import (ListOrdersSerializer,
                                                   OrderBase,
                                                   OrderCreateSerializer,
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
