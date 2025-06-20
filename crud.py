from sqlalchemy.orm import Session
from models import Item

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_all_items(db: Session):
    return db.query(Item).all()

def add_item(db: Session, name: str, store: str):
    db_item = Item(name=name, store=store)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_item(db: Session, name: str, store:str):
    item = db.query(Item).filter(Item.name == name and Item.store == store).first()
    if item:
        db.delete(item)
        db.commit()
        return True     
    return False


def remove_tab(db: Session, store:str):
    items = db.query(Item).filter(Item.store == store)
    if items:
        for item in items:
            db.delete(item)
            db.commit()
        return True     
    return False
