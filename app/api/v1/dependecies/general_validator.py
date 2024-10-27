from fastapi import  HTTPException
def validate_id(id: int)-> int:
    """
    Check cost to be 0< .
    Raise 400 if it's lower than 1.

    :param id: int
    :return: int
    """
    if id < 1:
        raise HTTPException(
            status_code=400, detail="Incorrect amount."
        )
    return id
