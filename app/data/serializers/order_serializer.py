from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    id: int
    creation_date: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)


class OrderCreateSerializer(BaseModel):
    creation_date: datetime
    status: str


class OrderUpdateStatusSerializer(BaseModel):
    id: int
    status: str


class ListOrdersSerializer(BaseModel):
    order_list: list[OrderBase]

    model_config = ConfigDict(from_attributes=True)
