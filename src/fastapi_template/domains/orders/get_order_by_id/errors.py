class OrderNotFoundError(Exception):
    """Raised when an order is not found in the database."""

    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"Order {order_id} not found")


class DatabaseError(Exception):
    """Generic error for database-related errors."""

    def __init__(self, message: str):
        super().__init__(message)
