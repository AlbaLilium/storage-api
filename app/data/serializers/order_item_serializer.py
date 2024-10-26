from pydantic import BaseModel, ConfigDict


class OrderItemBase(BaseModel):
    id: int
    product_id: int
    order_id: int
    product_amount: int

    model_config = ConfigDict(from_attributes=True)
