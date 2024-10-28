from fastapi import HTTPException

from app.data.enum import OrderStatusEnum


def is_status_correct(status: str) -> str:
    """
    Checks the string to see if it's enum value of OrderStatusEnum.

    :param status: str
    :return: str
    """
    if status not in [order_status_type.value for order_status_type in OrderStatusEnum]:
        raise HTTPException(status_code=400, detail="Incorrect order status")
    return status
