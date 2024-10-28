from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.api.v1.dependecies.general_validator import validate_id
from app.api.v1.dependecies.status_validator import \
    is_status_correct as correct_status


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

    _validate_id_id = field_validator("id")(validate_id)
    _validate_status_correct_status = field_validator("status")(correct_status)


class ListOrdersSerializer(BaseModel):
    order_list: list[OrderBase]

    model_config = ConfigDict(from_attributes=True)


class OrderItemBase(BaseModel):
    id: int
    product_id: int
    order_id: int
    product_amount: int

    model_config = ConfigDict(from_attributes=True)
