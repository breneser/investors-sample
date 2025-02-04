import csv
from datetime import datetime

from database import Session, create_tables, drop_tables
from database.models import Commitment, Investor

# Name to Investor mapping
investors: dict[str, Investor] = dict()


def create_investor(
    name: str,
    type: str,
    country: str,
    date_added: datetime,
    last_updated: datetime,
):
    """
    Create Investor and add to dictionary to prevent duplicate records

    Returns:
        Investor
    """
    investor = investors.get(name, None)
    if investor is None:
        investor = Investor(
            name=name,
            type=type,
            country=country,
            date_added=date_added,
            last_updated=last_updated,
            commitments=[],
        )
        investors[name] = investor

    return investor


def create_commitment(investor: Investor, asset_class: str, amount: int, currency: str):
    """
    Create Commitment for the investor

    Returns:
        Commitment
    """
    commitment = Commitment(asset_class=asset_class, amount=amount, currency=currency)
    investor.commitments.append(commitment)


def parse_csv():

    with open("scripts/data.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            investor = create_investor(
                name=row["Investor Name"],
                type=row["Investor Type"],
                country=row["Investor Country"],
                date_added=datetime.strptime(row["Investor Date Added"], "%Y-%m-%d"),
                last_updated=datetime.strptime(
                    row["Investor Last Updated"], "%Y-%m-%d"
                ),
            )
            create_commitment(
                investor=investor,
                asset_class=row["Commitment Asset Class"],
                amount=row["Commitment Amount"],
                currency=row["Commitment Currency"],
            )


if __name__ == "__main__":
    drop_tables()
    create_tables()
    parse_csv()
    with Session() as session:
        session.add_all(investors.values())
        session.commit()
