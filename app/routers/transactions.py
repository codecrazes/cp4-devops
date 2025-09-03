from typing import List
from fastapi import APIRouter, HTTPException

from app.dependencies import DBSession
from app.common.crud import create_transaction, delete_transaction, list_transactions, update_transaction
from app.common.schemas import TransactionCreate, TransactionOut, TransactionUpdate


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=List[TransactionOut])
def get_transactions(db: DBSession):
    return list_transactions(db)


@router.post("", response_model=TransactionOut, status_code=201)
def post_transaction(payload: TransactionCreate, db: DBSession):
    return create_transaction(db, payload)


@router.put("/{tx_id}", response_model=TransactionOut)
def put_transaction(tx_id: int, payload: TransactionUpdate, db: DBSession):
    updated = update_transaction(db, tx_id, payload)

    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return updated


@router.delete("/{tx_id}", status_code=204)
def del_transaction(tx_id: int, db: DBSession):
    ok = delete_transaction(db, tx_id)
    
    if not ok:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return
