from decimal import Decimal, ROUND_HALF_UP
from fastapi import  HTTPException

def validate_amount(amount: int)-> int:
    """
    Check cost to be 0< .
    Raise 400 if it's lower than 0.

    :param amount: int
    :return: int
    """
    if amount < 0:
        raise HTTPException(
            status_code=400, detail="Incorrect amount."
        )
    return amount

def validate_cost(cost: Decimal)->Decimal:
    """
    Check cost to be 0< .
    Raise 400 if it's lower than 0.


    :param cost: Decimal
    :return: decimal in template {0.00}
    """

    if cost < 0:
        raise  HTTPException(
            status_code=400, detail= "Incorrect cost. "
        )
    cents = Decimal("0.01")

    return cost.quantize(cents, ROUND_HALF_UP)



def validate_text(text:str)->str:
    """
     Check string on being empty.

     Raise 400 if it is empty.

    :param text: str
    :return: str
    """
    if text == '':
        raise HTTPException(
            status_code=400, detail= "Field shouldn't be empty"
            )
    return text
