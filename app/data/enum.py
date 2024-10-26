import enum


class OrderStatusEnum(enum.Enum):
    get_order = "receive order"
    send_order = "sent"
    order_delivered = "delivered"
