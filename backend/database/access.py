from sqlalchemy import func, select
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

    def get(self, offset: int = 0, limit: int = 10) -> list[schemas.Investor]:
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

    def _get(
        self,
        offset: int,
        limit: int,
        investor_id: int | None = None,
        asset_class=None,
    ):
        statement = select(models.Commitment).limit(limit).offset(offset)
        if investor_id:
            statement = statement.filter_by(investor_id=investor_id)

        if asset_class:
            statement = statement.filter_by(asset_class=asset_class)

        return [
            schemas.Commitment.model_validate(commitment)
            for commitment in self.session.scalars(statement)
        ]

    def get(self, offset: int = 0, limit: int = 10) -> list[schemas.Commitment]:
        """
        Read and return list of Commitments from the db with given limit
        """
        return self._get(offset, limit)

    def get_by_investor(
        self,
        investor_id: int,
        asset_class: str | None,
        offset: int = 0,
        limit: int = 10,
    ):
        return self._get(
            offset,
            limit,
            investor_id=investor_id,
            asset_class=asset_class,
        )

    def get_asset_totals(self, investor_id: int):

        return [
            schemas.AssetTotals.model_validate(
                {"asset_class": row[0], "total_commitment": row[1]}
            )
            for row in (
                self.session.query(
                    models.Commitment.asset_class,
                    func.sum(models.Commitment.amount).label("total_commitment"),
                )
                .group_by(models.Commitment.asset_class)
                .filter_by(investor_id=investor_id)
            )
        ]
