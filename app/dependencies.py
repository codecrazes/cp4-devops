from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.common.database import Database

from .common.config import settings

db = Database(settings.database_url)
DBSession = Annotated[Session, Depends(db)]
