from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import create_tables, open_session
from database.access import InvestorAccessor

app = FastAPI()

Session = Annotated[Session, Depends(open_session)]


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/investors")
def get_investors(session: Session, page: int = 1):
    # 10 items per page by default, TODO: make configurable?
    return InvestorAccessor(session).get_offset(
        offset=(page - 1) * 10,
        limit=10,
    )
