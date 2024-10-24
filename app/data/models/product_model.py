from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db_connection import Base


class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    cost: Mapped[float] = mapped_column(
        Float(precision=15, asdecimal=True, decimal_return_scale=2), nullable=False
    )
    amount: Mapped[int] = mapped_column(Integer)
