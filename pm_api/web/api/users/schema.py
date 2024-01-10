from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """Simple user model."""

    id: Optional[int] = None
    name: str
    email: str
    is_active: bool
