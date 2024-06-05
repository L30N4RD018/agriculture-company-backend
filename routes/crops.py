from fastapi import APIRouter, Depends
from pydantic import BaseModel
from controllers.crops_controller import CropsController
from logic.crop import Crop
from datetime import date

class CropModel(BaseModel):
    id: int
    type: str
    state: str
    sow_date: date
    harvest_date: date
    storage_id: int
    smallholding_id: int
    quantity: int


router = APIRouter()
CC = CropsController()

@router.get("/api/crops", tags=["Crops"])
async def get_crops():
    return CC.show_crops()

@router.get("/api/crops/{id}", tags=["Crops"], response_model=CropModel)
async def get_crop(id: int):
    return CC.search_crop(id)

@router.get("/api/crops/months", tags=["Crops"])
async def get_crops_months():
    return CC.show_crops_months()

@router.post("/api/crops", tags=["Crops"], response_model=CropModel)
async def post_crop(crop_model: CropModel):
    return CC.add_crop(Crop(**crop_model.model_dump()))

@router.put("/api/crops", tags=["Crops"], response_model=CropModel)
async def put_crop(crop_model: CropModel):
    return CC.update_crop(Crop(**crop_model.model_dump()))

@router.delete("/api/crops/{id}", tags=["Crops"], response_model=CropModel)
async def delete_crop(id: int):
    return CC.delete_crop(id)