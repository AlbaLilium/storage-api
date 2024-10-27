from decimal import ROUND_HALF_UP, Decimal

from fastapi import HTTPException


def validate_amount(amount: int) -> int:
    """
    Check cost to be 0< .

    :param amount: int
    :raise HTTPException 400
        if amount is lower than 0.
    :return: int
    """
    if amount < 0:
        raise HTTPException(status_code=400, detail="Incorrect amount.")
    return amount


def validate_cost(cost: Decimal) -> Decimal:
    """
    Check cost to be 0< .

    :param cost: Decimal

    :raise HTTPException 400
     if cost lower than 0

    :return: decimal in template {0.00}
    """

    if cost < 0:
        raise HTTPException(status_code=400, detail="Incorrect cost. ")
    cents = Decimal("0.01")

    return cost.quantize(cents, ROUND_HALF_UP)


def validate_text(text: str) -> str:
    """
     Check string on being empty.

    :param text: str
    :raise HTTPException 400 if it is empty.
    :return: str
    """
    if text == "":
        raise HTTPException(status_code=400, detail="Field shouldn't be empty")
    return text


def validate_numeric_values(cost: Decimal, amount: int) -> bool:
    """

    :param cost: int

    :param amount: int

    :raise HTTPException
    :return: bool
    """
    if cost:
        cost = validate_cost(cost)
    elif amount:
        amount = validate_amount(amount)
    return True
