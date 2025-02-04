from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import create_tables, open_session
from database.access import CommitmentAccessor, InvestorAccessor

app = FastAPI()

Session = Annotated[Session, Depends(open_session)]


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/investors")
def get_investors(session: Session, page: int = 1):
    # 10 items per page by default, TODO: make configurable?
    page = page if page > 0 else 1
    investors = InvestorAccessor(session).get(
        offset=(page - 1) * 10,
        limit=10,
    )

    if not investors:
        raise HTTPException(status_code=404, detail="Page not found")

    return investors


@app.get("/investors/{investor_id}/commitments")
def get_commitments(session: Session, investor_id: int, page: int = 1):
    # 10 items per page by default, TODO: make configurable?
    page = page if page > 0 else 1
    commitments = CommitmentAccessor(session).get_by_investor(
        investor_id=investor_id,
        offset=(page - 1) * 10,
        limit=10,
    )
    if not commitments:
        raise HTTPException(status_code=404, detail="Page not found")

    return commitments


# @app.get("/investors/{id}/asset_classes")
# def get_asset_classes(
#     session: Session,
#     asset_class: str = "",
# ):
#     commitments = CommitmentAccessor(session).get_offset(
#         offset=(page - 1) * 10, limit=10
#     )
#     if not commitments:
#         raise HTTPException(status_code=404, detail="Page not found")
#
#     return commitments
