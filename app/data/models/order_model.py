from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db_connection import Base


class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    creation_date: Mapped[DateTime] = mapped_column(
        DateTime, nullable=True, default=datetime.now(UTC)
    )
    status = mapped_column(String(20), nullable=False)


class OrderItem(Base):
    __tablename__ = "orderitem"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE")
    )
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"))
    product_amount: Mapped[int] = mapped_column(Integer)
