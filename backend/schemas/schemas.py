"""
Pydantic schemas are serialisable and automatically serialised by FastAPI
making them ideal to use with API endpoints as well.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

__all__ = ["Investor", "Commitment"]


class Investor(BaseModel):
    """
    Schema for investor instances, to utilise on layers above data access.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int | None
    name: str
    type: str
    country: str
    date_added: datetime
    last_updated: datetime
    total_commitment: int

    def __eq__(self, other):
        return self.name == other.name


class Commitment(BaseModel):
    """
    Schema for investor instances, to utilise on layers above data access.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int | None
    asset_class: str
    amount: int
    currency: str
