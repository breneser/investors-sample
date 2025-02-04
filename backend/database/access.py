from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas

from . import models


class InvestorAccessor:
    """Investor database access object

    Attributes:
        session: database session
    """

    def __init__(self, session: Session):
        self.session = session

    def get_offset(self, offset: int = 0, limit: int = 10) -> list[schemas.Investor]:
        """
        Read and return list of Investors from the db with given limit
        """
        return [
            schemas.Investor.model_validate(investor)
            for investor in self.session.scalars(
                select(models.Investor).limit(limit).offset(offset)
            ).all()
        ]


class CommitmentAccessor:
    """Commitment database access object

    Attributes:
        session: database session
    """

    def __init__(self, session: Session):
        self.session = session

    def get_offset(self, offset: int = 0, limit: int = 10) -> list[schemas.Commitment]:
        """
        Read and return list of Commitments from the db with given limit
        """
        return [
            schemas.Commitment.model_validate(commitment)
            for commitment in self.session.scalars(
                select(models.Commitment).limit(limit).offset(offset)
            )
        ]
