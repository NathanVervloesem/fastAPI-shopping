from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

DATA_FILE = "data.json"

class Item(BaseModel):
    name: str
    store: str

# Ensure the file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.get("/items/")
def get_items():
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    

@app.post("/items/remove")
def remove_item(item: Item):
    with open(DATA_FILE, "r") as f:
        items = json.load(f)

    new_items = []
    count = 0
    for i in items:
        if i["name"] == item.name and i["store"] == item.store and count==0:
            count = count + 1
        else:
            new_items.append(i)
    count = 0

    #new_items = [ i for i in items if i["name"] != item.name ]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    with open(DATA_FILE, "w") as f:
        json.dump(new_items, f, indent=2)
    return {"message": f"Removed item: {item.name}"}  
    
@app.post("/items/add")
def add_item(item: Item):
    with open(DATA_FILE, "r") as f:
        items = json.load(f)
    items.append(item.model_dump())
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=2)
    return {"message": "Item added"}


@app.post("/items/clear_tab")
def clear_tab(item: Item):
    with open(DATA_FILE, "r") as f:
        items = json.load(f)    
    new_items = [ i for i in items if i["store"] != item.store ]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Store not found")
    with open(DATA_FILE, "w") as f:
        json.dump(new_items, f, indent=2)
    return {"message": f"Removed item of store: {item.store}"}       


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

