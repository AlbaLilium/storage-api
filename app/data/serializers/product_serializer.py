from decimal import Decimal
from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    """
    Base Serializer for Product.

     ...

     Attributes
     ----------
      id: int
      title: str | None
      description: str | None
      cost: Decimal| None
      amount: int| None

      Notes
      ------
       ORM reading is supported.
    """

    id: int
    title: str
    description: str
    cost: Decimal
    amount: int

    model_config = ConfigDict(from_attributes = True)


class ListProductSerializer(BaseModel):
    """
    Base Serializer for Product.

     ...

     Attributes
     ----------
       product_list: list[ProductBase]


    """

    product_list: list[ProductBase]


class UpdateProductSerializer(BaseModel):
    """
    Product serializer for updating requests.
         ...

         Attributes
         ----------
          id: int
          title: str | None
          description: str | None
          cost: Decimal| None
          amount: int| None

    """

    id: int
    title: str | None
    description: str | None
    cost: Decimal | None
    amount: int | None

    def validate_entity(self):
        if self.cost < 0 or self.amount < 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect data."
            )


class CreateProductSerializer(BaseModel):
    """
    Product serializer for creating requests.

     ...

     Attributes
     ----------
      title: str | None
      description: str | None
      cost: Decimal| None
      amount: int| None

    """

    title: str
    description: str
    cost: Decimal
    amount: int

    def validate_entity(self):
        details = {"numbers": "Can't be less than 0", "strings": "can't be empty"}
        if self.cost < 0 or self.amount < 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail=details["numbers"]
            )
        elif self.description:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail=details["strings"]
            )
        elif self.title:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail=details["strings"]
            )
