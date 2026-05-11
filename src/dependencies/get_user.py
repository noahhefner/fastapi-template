from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    """User information."""

    id: UUID
    username: str
    display_name: str


def get_user() -> User:
    """Get user info.

    In a real application, this dependency could extract an access token from the request and/or
    lookup the users info from a database. For demonstration purposes, this function simply returns
    a demo user object.
    """

    return User(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        username="demo_user",
        display_name="Demo User",
    )
