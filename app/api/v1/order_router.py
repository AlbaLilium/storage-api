from datetime import UTC, datetime

from fastapi import APIRouter

from app.api.v1.dependecies.status_validator import is_status_correct
from app.controllers.queries.order_item_queries import OrderItemOperation
from app.controllers.queries.order_queries import OrderOperation
from app.controllers.queries.product_queries import ProductOperation
from app.data.enum import OrderStatusEnum
from app.data.serializers.order_serializer import (ListOrdersSerializer,
                                                   OrderBase,
                                                   OrderCreateSerializer,
                                                   OrderUpdateStatusSerializer)

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post("")
async def create_order(product_id: int, product_amount: int):
    async with OrderOperation() as db:
        new_order = OrderCreateSerializer(
            status=OrderStatusEnum.get_order.value, creation_date=datetime.now(UTC)
        )
        order_id = await db.create_order(new_order=new_order)

    async with OrderItemOperation() as db:
        order_item = await db.create_order_item(
            order_id=order_id, product_id=product_id, product_amount=product_amount
        )

    async with ProductOperation() as db:
        product = await db.get_product(product_id=product_id)
    return {"order": new_order, "order_item": order_item, "product": product}


@order_router.get("", response_model=ListOrdersSerializer)
async def get_all_orders():
    async with OrderOperation() as db:
        orders_list = await db.get_all_orders()
    return orders_list


@order_router.get("/{id}", response_model=OrderBase)
async def get_order(order_id: int):
    async with OrderOperation() as db:
        order = await db.get_order(order_id=order_id)
    return order


@order_router.patch("/{id}", response_model=OrderBase)
async def update_status(status_update: OrderUpdateStatusSerializer):
    if is_status_correct(status_update.status):
        async with OrderOperation() as db:
            updated_order = await db.update_status(new_status=status_update)
        return updated_order
