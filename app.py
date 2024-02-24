from logic.state import SownState, GermidatedState, StoragedState, DeliveringState, DeliveriedState
from controllers.delivery_details_crontroller import DeliveryDetailsController
from controllers.smallholding_controller import SmallholdingsController
from controllers.delivery_controller import DeliveryController
from controllers.storage_controller import StoragesController
from controllers.users_controller import UsersController
from controllers.crop_controller import CropsController
from starlette.middleware.cors import CORSMiddleware
from logic.delivery_details import DeliveryDetails
from logic.smallholding import Smallholding
from logic.delivery import Delivery
from fastapi import FastAPI, Query
from logic.storage import Storage
from logic.crop import Crop
from datetime import date
import uvicorn

app = FastAPI()

origins = ["*"]

CC = CropsController()
SC = SmallholdingsController()
STC = StoragesController()
DC = DeliveryController()
DDC = DeliveryDetailsController()
UC = UsersController()
STATES = {
    "Sown": SownState(),
    "Germidated": GermidatedState(),
    "Storaged": StoragedState(),
    "Delivering": DeliveringState(),
    "Delivered": DeliveriedState()
}

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"200": "Welcome to Agriculture Company API"}

@app.get("/crops")
async def read_crops():
    return CC.show_crops()

@app.get("/crops/{id}")
async def search_crop(id: int):
    return CC.search_crop(id)

@app.get("/crops_by_month")
async def read_crops_by_month():
    return CC.show_crops_by_date()

@app.get("/crops_by_smallholding/{id}")
async def read_crops_by_smallholding(id: int):
    return CC.show_crops_by_smallholding(id)

@app.get("/crops_by_storage/{id}")
async def read_crops_by_storage(id: int):
    return CC.show_crops_by_storage(id)

@app.post("/crops")
async def create_crop(type: str = Query(None, min_length=1, max_length=50,description="Crop Type"),
                      state: str = Query(None, min_length=4, description="Crop State"),
                      sow_date: date = Query(date.today(), description="Crop Sow Date"),
                      harvest_date: date = Query(None, description="Crop Harvest Date"),
                      storage_id: int = Query(None, description="Storage ID"),
                      smallholding_id: int = Query(None, description="Smallholding ID"),
                      quantity: int = Query(None, description="Crop Quantity")):
    crop = Crop(None, type, STATES[state], sow_date, harvest_date, storage_id, smallholding_id, quantity)                      
    return CC.insert_crop(crop)

@app.put("/crops/{id}")
async def update_crop(id: int,
                      type: str = Query(None, min_length=1, max_length=50,description="Crop Type"),
                      state: str = Query(None, min_length=4, description="Crop State"),
                      sow_date: date = Query(date.today(), description="Crop Sow Date"),
                      harvest_date: date = Query(date.today(), description="Crop Harvest Date"),
                      storage_id: int = Query(None, description="Storage ID"),
                      smallholding_id: int = Query(None, description="Smallholding ID"),
                      quantity: int = Query(None, description="Crop Quantity")):
    crop = Crop(id, type, STATES[state], sow_date, harvest_date, storage_id, smallholding_id, quantity)                      
    return CC.update_crop(crop)

@app.delete("/crops/{id}")
async def delete_crop(id: int):
    return CC.delete_crop(id)

@app.get("/smallholdings")
async def read_smallholdings():
    return SC.show_smallholdings()

@app.get("/smallholdings/{id}")
async def search_smallholding(id: int):
    return SC.search_smallholding(id)

@app.post("/smallholdings")
async def create_smallholding(size: float = Query(None, description="Smallholding Size"),
                              ubication: str = Query(None, min_length=1, max_length=50, description="Smallholding Ubication"),
                              shape: str = Query(None, min_length=1, max_length=50, description="Smallholding Shape"),
                              delimited: bool = Query(True, description="Smallholding Delimited")):
    smallholding = Smallholding(None, size, ubication, shape, delimited)
    return SC.insert_smallholding(smallholding)

@app.put("/smallholdings/{id}")
async def update_smallholding(id: int,
                              size: float = Query(None, description="Smallholding Size"),
                              ubication: str = Query(None, min_length=1, max_length=50, description="Smallholding Ubication"),
                              shape: str = Query(None, min_length=1, max_length=50, description="Smallholding Shape"),
                              delimited: bool = Query(True, description="Smallholding Delimited")):
    smallholding = Smallholding(id, size, ubication, shape, delimited)
    return SC.update_smallholding(smallholding)

@app.delete("/smallholdings/{id}")
async def delete_smallholding(id: int):
    return SC.delete_smallholding(id)

@app.get("/storages")
async def read_storages():
    return STC.show_storages()

@app.get("/storages/{id}")
async def search_storage(id: int):
    return STC.search_storage(id)

@app.post("/storages")
async def create_storage(max_capacity: float = Query(None, description="Storage Max Capacity"),
                         current_capacity: float = Query(None, description="Storage Current Capacity"),
                         ubication: str = Query(None, min_length=1, max_length=50, description="Storage Ubication"),
                         equipment: str = Query(None, min_length=1, max_length=50, description="Storage Equipment")):
    storage = Storage(None, max_capacity, current_capacity, ubication, equipment)
    return STC.insert_storage(storage)

@app.put("/storages/{id}")
async def update_storage(id: int,
                         max_capacity: float = Query(None, description="Storage Max Capacity"),
                         current_capacity: float = Query(None, description="Storage Current Capacity"),
                         ubication: str = Query(None, min_length=1, max_length=50, description="Storage Ubication"),
                         equipment: str = Query(None, min_length=1, max_length=50, description="Storage Equipment")):
    storage = Storage(id, max_capacity, current_capacity, ubication, equipment)
    return STC.update_storage(storage)

@app.delete("/storages/{id}")
async def delete_storage(id: int):
    return STC.delete_storage(id)

@app.get("/deliveries")
async def read_deliveries():
    return DC.show_deliveries()

@app.get("/deliveries/{id}")
async def search_delivery(id: int):
    return DC.search_delivery(id)

@app.get("/deliveries_by_month")
async def read_deliveries_by_date():
    return DC.show_deliveries_by_date()

@app.post("/deliveries")
async def create_delivery(client_name: str = Query(None, min_length=1, max_length=50, description="Delivery Client Name"),
                          deliver_date: date = Query(date.today(), description="Delivery Deliver Date"),
                          request_date: date = Query(date.today(), description="Delivery Request Date"),
                          address: str = Query(None, min_length=1, max_length=50, description="Delivery Address")):
    delivery = Delivery(None, client_name, deliver_date, request_date, address)
    return DC.insert_delivery(delivery)

@app.put("/deliveries/{id}")
async def update_delivery(id: int,
                          client_name: str = Query(None, min_length=1, max_length=50, description="Delivery Client Name"),
                          deliver_date: date = Query(date.today(), description="Delivery Deliver Date"),
                          request_date: date = Query(date.today(), description="Delivery Request Date"),
                          address: str = Query(None, min_length=1, max_length=50, description="Delivery Address")):
    delivery = Delivery(id, client_name, deliver_date, request_date, address)
    return DC.update_delivery(delivery)

@app.delete("/deliveries/{id}")
async def delete_delivery(id: int):
    return DC.delete_delivery(id)

@app.get("/delivery_details")
async def read_delivery_details():
    return DDC.show_deliveries_details()

@app.get("/delivery_details/{id}")
async def search_delivery_details(id: int):
    return DDC.search_delivery_details(id)

@app.post("/delivery_details")
async def create_delivery_details(delivery_id: int = Query(None, description="Delivery ID"),
                                 crop_id: int = Query(None, description="Crop ID"),
                                 quantity: int = Query(None, description="Delivery Details Quantity")):
    delivery_details = DeliveryDetails(None, delivery_id, crop_id, quantity)
    return DDC.insert_delivery_details(delivery_details)

@app.put("/delivery_details/{id}")
async def update_delivery_details(id: int,
                                 delivery_id: int = Query(None, description="Delivery ID"),
                                 crop_id: int = Query(None, description="Crop ID"),
                                 quantity: int = Query(None, description="Delivery Details Quantity")):
    delivery_details = DeliveryDetails(id, delivery_id, crop_id, quantity)
    return DDC.update_delivery_details(delivery_details)

@app.delete("/delivery_details/{id}")
async def delete_delivery_details(id: int):
    return DDC.delete_delivery_details(id)

@app.get("/users")
async def read_users():
    return UC.show_users()

@app.get("/users/{email}")
async def search_user(email: str):
    return UC.search_user(email)

@app.post("/users")
async def create_user(email: str = Query(None, min_length=1, max_length=50, description="User Email"),
                      rol: str = Query(None, min_length=1, max_length=50, description="User Rol")): 
    return UC.insert_user(email, rol)

@app.put("/users/{id}")
async def update_user(id: int,
                      email: str = Query(None, min_length=1, max_length=50, description="User Email"),
                      rol: str = Query(None, min_length=1, max_length=50, description="User Rol")):
    return UC.update_user(id, email, rol)

@app.delete("/users/{id}")
async def delete_user(id: int):
    return UC.delete_user(id)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)