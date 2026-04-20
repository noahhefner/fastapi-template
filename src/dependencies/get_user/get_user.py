from uuid import UUID

from .models.user import User


def get_user() -> User:
    """Get user info.

    In a real application, this dependency could extract an access token from the request and lookup
    the user in the database. For demonstration purposes, this function simply returns a demo user
    object.
    """

    return User(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        username="demo_user",
        display_name="Demo User",
    )
