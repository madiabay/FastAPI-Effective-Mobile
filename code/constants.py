from enum import Enum


class OrderStatus(Enum):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    PAID = 'PAID'
    CANCELLED = 'CANCELLED'
    SENT = 'SENT'
