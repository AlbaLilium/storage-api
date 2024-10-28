from datetime import UTC, datetime

from fastapi import APIRouter

from app.api.v1.dependecies.general_validator import validate_id
from app.api.v1.dependecies.product_validator import validate_amount
from app.controllers.queries.order import OrderItemOperation, OrderOperation
from app.controllers.queries.product import ProductOperation
from app.data.enum import OrderStatusEnum
from app.data.serializers.order import (ListOrdersSerializer, OrderBase,
                                        OrderCreateSerializer,
                                        OrderUpdateStatusSerializer)

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post("")
async def create_order(product_id: int, product_amount: int):
    """
    Create order for specific product.

    :raise HTTPError 400 for
        id < 0,
        product_amount < 1,
        product_amount is more than warehouse has.

    :param
        product_id: int
        product_amount: int

    :return: dict["order": OrderBase, "order_item": OrderItemBase, "product": ProductBase]
    """
    async with OrderOperation() as db:
        new_order = OrderCreateSerializer(
            status=OrderStatusEnum.get_order.value, creation_date=datetime.now(UTC)
        )
        order_id = await db.create_order(new_order=new_order)

    async with OrderItemOperation() as db:
        order_item = await db.create_order_item(
            order_id=order_id,
            product_id=validate_id(product_id),
            product_amount=validate_amount(product_amount),
        )

    async with ProductOperation() as db:
        product = await db.get_product(product_id=product_id)
    return {"order": new_order, "order_item": order_item, "product": product}


@order_router.get("", response_model=ListOrdersSerializer)
async def get_all_orders():
    """
    Get all orders.

    :return: [OrderBase]
    """
    async with OrderOperation() as db:
        orders_list = await db.get_all_orders()
    return orders_list


@order_router.get("/{id}", response_model=OrderBase)
async def get_order(order_id: int):
    """
    Get a specific order by id.

    :param order_id: int

    :raise HTTPError 400 if:
         id < 0.

    :return: OrderBase:
        id: int
        creation_date: datetime
        status: str

    """
    async with OrderOperation() as db:
        order = await db.get_order(order_id=validate_id(order_id))
    return order


@order_router.patch("/{id}", response_model=OrderBase)
async def update_status(status_update: OrderUpdateStatusSerializer):
    """

    :param status_update:
        id: int
        status: "receive order", "sent", "delivered"

    :raise HTTPError 400:
        if status is incorrect
        id < 0

    :return: OrderBase
    """
    async with OrderOperation() as db:
        updated_order = await db.update_status(new_status=status_update)
        return updated_order
