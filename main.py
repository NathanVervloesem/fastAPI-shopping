from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from sqlalchemy.orm import Session
import models
import database
import crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fastapi-shopping-1.onrender.com", ],  # Use specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=database.engine)


# class Item(BaseModel):
#     name: str
#     store: str

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/ping')
def ping():
    return {"status":"ok"}


@app.get("/items/")
def get_items(db: Session = Depends(get_db)):
    db_items = list(crud.get_all_items(db))
    if db_items is None:
        raise HTTPException(status_code=404, detail="Items not found")
    return db_items

@app.post("/items/add")
def add_item_route(name: str, store: str, db: Session = Depends(get_db)):
    return crud.add_item(db, name, store)

@app.post("/items/remove")
def remove_item_route(name: str, store: str, db: Session = Depends(get_db)):
    success = crud.remove_item(db, name, store)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": f"Item {name, store} deleted"}

@app.post("/items/clear_tab")
def clear_tab(store: str, db: Session = Depends(get_db)):
    success = crud.remove_tab(db, store)
    if not success:
        raise HTTPException(status_code=404, detail="Items not found")

#TODO make post  for clear tab 

#------------------------

# DATA_FILE = "data.json"

# class Item(BaseModel):
#     name: str
#     store: str

# # Ensure the file exists
# if not os.path.exists(DATA_FILE):
#     with open(DATA_FILE, "w") as f:
#         json.dump([], f)

# @app.get('/ping')
# def ping():
#     return {"status":"ok"}

# @app.get("/items/")
# def get_items():
#     with open(DATA_FILE, "r") as f:
#         return json.load(f)
    

# @app.post("/items/remove")
# def remove_item(item: Item):
#     with open(DATA_FILE, "r") as f:
#         items = json.load(f)

#     new_items = []
#     count = 0
#     for i in items:
#         if i["name"] == item.name and i["store"] == item.store and count==0:
#             count = count + 1
#         else:
#             new_items.append(i)
#     count = 0

#     #new_items = [ i for i in items if i["name"] != item.name ]
#     if len(new_items) == len(items):
#         raise HTTPException(status_code=404, detail="Item not found")
#     with open(DATA_FILE, "w") as f:
#         json.dump(new_items, f, indent=2)
#     return {"message": f"Removed item: {item.name}"}  
    
# @app.post("/items/add")
# def add_item(item: Item):
#     with open(DATA_FILE, "r") as f:
#         items = json.load(f)
#     items.append(item.model_dump())
#     with open(DATA_FILE, "w") as f:
#         json.dump(items, f, indent=2)
#     return {"message": "Item added"}


# @app.post("/items/clear_tab")
# def clear_tab(item: Item):
#     with open(DATA_FILE, "r") as f:
#         items = json.load(f)    
#     new_items = [ i for i in items if i["store"] != item.store ]
#     if len(new_items) == len(items):
#         raise HTTPException(status_code=404, detail="Store not found")
#     with open(DATA_FILE, "w") as f:
#         json.dump(new_items, f, indent=2)
#     return {"message": f"Removed item of store: {item.store}"}       

#-------------

# @app.post("/")
# def add_item():
#     new_user = User(name=name, email=email)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get("/")
# def read_items():
#     try:
#         f = open("items.txt")
#         msg = []
#         for line in f:
#             msg.append(line)
#     except:
#         print("The file you want to read doesn't exist")
#     finally:
#         f.close()

#     return {"status": "success", "message": f"Thanks for the data, {msg}!"}

