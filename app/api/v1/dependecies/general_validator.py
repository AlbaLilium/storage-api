from fastapi import HTTPException


def validate_id(id: int) -> int:
    """
    Check id to be more than 1.

    :param id: int
    :raise HTTPException 400
        if id value is  lower than 1.
    :return: int
    """
    if id < 1:
        raise HTTPException(status_code=400, detail="Incorrect id.")
    return id
