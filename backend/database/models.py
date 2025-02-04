from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Investor(Base):
    """
    Database model for an Investor.
    With given scope and in the interest of time not creating a separate model
    for the 'type' of investor as it is not dynamically managed.
    Same goes for country.

    """

    __tablename__ = "investors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    type: Mapped[str] = mapped_column()  # TODO: Use enum
    country: Mapped[str] = mapped_column()  # TODO: Use enum?
    # Assuming no timezone with dates
    date_added: Mapped[datetime] = mapped_column()
    last_updated: Mapped[datetime] = mapped_column()

    commitments: Mapped[list["Commitment"]] = relationship(
        back_populates="investor", cascade="all,delete-orphan", lazy="subquery"
    )

    @property
    def total_commitment(self) -> int:
        return sum([commitment.amount for commitment in self.commitments])

    def __repr__(self):
        return f"Investor: {self.name} - {self.type} - {self.country}"


class Commitment(Base):
    """Database model for investor commitment for an asset class."""

    __tablename__ = "commitments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    # Asset class doesn't seem to be varied enough to require an index
    # Index probably won't be used even if created.
    asset_class: Mapped[str] = mapped_column()  # TODO: use enum
    amount: Mapped[int] = mapped_column()
    currency: Mapped[str] = mapped_column(default="GBP")

    investor_id: Mapped[int] = mapped_column(ForeignKey("investors.id"))
    investor: Mapped[Investor] = relationship(back_populates="commitments")

    def __repr__(self):
        return f"Commitment: {self.asset_class} - {self.amount}"
