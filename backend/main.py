from typing import Annotated

from database import create_tables, open_session
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

Session = Annotated[Session, Depends(open_session)]


@app.on_event("startup")
def on_startup():
    create_tables()
