from typing import List, Optional

from sqlalchemy.orm import Session

from .models import Transaction
from .schemas import TransactionCreate, TransactionUpdate


def list_transactions(db: Session) -> List[Transaction]:
    return db.query(Transaction).order_by(Transaction.id.desc()).all()


def create_transaction(db: Session, payload: TransactionCreate) -> Transaction:
    tx = Transaction(descricao=payload.descricao, valor=payload.valor)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def update_transaction(
    db: Session, tx_id: int, payload: TransactionUpdate
) -> Optional[Transaction]:
    tx = db.get(Transaction, tx_id)
    if not tx:
        return None
    if payload.descricao is not None:
        tx.descricao = payload.descricao
    if payload.valor is not None:
        tx.valor = payload.valor
    db.commit()
    db.refresh(tx)
    return tx


def delete_transaction(db: Session, tx_id: int) -> bool:
    tx = db.get(Transaction, tx_id)
    if not tx:
        return False
    db.delete(tx)
    db.commit()
    return True
