class OrderNotFoundError(Exception):
    """Raised when an order is not found in the database."""

    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"Order {order_id} not found")
