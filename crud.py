from sqlalchemy.orm import Session
from sqlalchemy import exc
from models import Item
from functools import wraps
from exeption_db_decorator import handle_db_errors
from DB_sesion_manager import DBSessionManager

# CREATE


@handle_db_errors
def create_item(db: Session, name: str, description: str):
    item = Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
# READ


@handle_db_errors
def get_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    return item


@handle_db_errors
def get_items(db: Session):
    return db.query(Item).all()

# UPDATE


@handle_db_errors
def update_item(
    db: Session,
    item_id: int,
    name: str = None,
    description: str = None
):
    # first form of update - Consulta cruda  - no soporta funcionalidades del orm
    # update_stmt = (Update(Item)
    #                .where(Item.id == item_id)
    #                .values(name=name, description=description))
    # db.execute(update_stmt)

    # second form- forma natva del ORM
    item = db.query(Item).filter(Item.id == item_id).first()
    item.name = name
    item.description = description

    # # third form - enfoque mixto - solo se utilizan una funciones del ORM
    # db.query(Item).filter(Item.id == item_id).update({
    #     "name": name,
    #     "description": description
    # })

    db.commit()

# DELETE


@handle_db_errors
def delete_item(db: Session, item_id: int):
    # Guarda el item en memoria - soporta funcionalidades del orm
    item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(item)

    # no guarda en memoria el item - no soporta funcionalidades del orm
    # db.delete(db.query(Item).filter(Item.id == item_id).first())

    db.commit()
