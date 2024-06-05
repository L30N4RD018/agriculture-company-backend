from controllers.storage_controller import StorageController
from fastapi import APIRouter, Depends
from logic.storage import Storage
from pydantic import BaseModel

router = APIRouter()
SC = StorageController()
TAGS = ["Storages"]

class StorageModel(BaseModel):
    id: int
    max_capacity: float
    current_capacity: float    
    storage_ubication: str
    equipment: str

@router.get("/api/storages", tags=TAGS)
async def storages():
    return SC.show_storages()

@router.get("/api/storages/crops/{id}", tags=TAGS)
async def storage_crops(id: int):
    return SC.show_storage_crops(id)

@router.get("/api/storages/{id}", tags=TAGS, response_model=StorageModel)
async def search_storage(id: int):
    return SC.search_storage(id)

@router.post("/api/storages", tags=TAGS, response_model=StorageModel)
async def add_storage(storage_model: StorageModel):
    return SC.add_storage(Storage(**storage_model.model_dump()))

@router.put("/api/storages", tags=TAGS, response_model=StorageModel)
async def update_storage(storage_model: StorageModel):
    return SC.update_storage(Storage(**storage_model.model_dump()))

@router.delete("/api/storages/{id}", tags=TAGS, response_model=StorageModel)
async def delete_storage(id: int):
    return SC.delete_storage(id)