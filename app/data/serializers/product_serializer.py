from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator

from app.api.v1.dependecies.general_validator import validate_id
from app.api.v1.dependecies.product_validator import (validate_amount,
                                                      validate_cost,
                                                      validate_text)


class ProductBase(BaseModel):
    id: int
    title: str
    description: str
    cost: Decimal
    amount: int

    model_config = ConfigDict(from_attributes=True)


class ListProductSerializer(BaseModel):
    product_list: list[ProductBase]


class UpdateProductSerializer(BaseModel):
    id: int
    title: str | None
    description: str | None
    cost: Decimal | None
    amount: int | None

    _validate_id_id = field_validator("id")(validate_id)


class CreateProductSerializer(BaseModel):
    title: str
    description: str
    cost: Decimal
    amount: int

    _validate_text_title = field_validator("title")(validate_text)
    _validate_text_description = field_validator("description")(validate_text)
    _validate_cost_cost = field_validator("cost")(validate_cost)
    _validate_amount_amount = field_validator("amount")(validate_amount)
