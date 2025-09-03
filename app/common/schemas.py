from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    descricao: str = Field(..., max_length=255)
    valor: float


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    descricao: Optional[str] = Field(None, max_length=255)
    valor: Optional[float] = None


class TransactionOut(TransactionBase):
    id: int
    data_transacao: datetime

    class Config:
        from_attributes = True
