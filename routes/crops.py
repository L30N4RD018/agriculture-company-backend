from fastapi import APIRouter
from pydantic import BaseModel
from controllers.crop_controller import CropsController
from logic.crop import Crop
from datetime import date

class CropModel(BaseModel):
    id: int | None = None
    type: str
    state: str
    sow_date: date | None = None
    harvest_date: date | None = None
    storage_id: int | None = None
    smallholding_id: int | None = None
    quantity: int


router = APIRouter()
CC = CropsController()

@router.get("/api/crops", tags=["Crops"])
async def get_crops():
    return CC.show_crops()

@router.get("/api/crops/months", tags=["Crops"])
async def get_crops_months():
    return CC.show_crops_month()

@router.get("/api/crops/{id}", tags=["Crops"], response_model=CropModel)
async def get_crop(id: int):
    return CC.search_crop(id)

@router.post("/api/crops", tags=["Crops"], response_model=CropModel)
async def post_crop(crop_model: CropModel):
    return CC.add_crop(Crop(**crop_model.model_dump()))

@router.put("/api/crops", tags=["Crops"], response_model=CropModel)
async def put_crop(crop_model: CropModel):
    return CC.update_crop(Crop(**crop_model.model_dump()))

@router.delete("/api/crops/{id}", tags=["Crops"], response_model=CropModel)
async def delete_crop(id: int):
    return CC.delete_crop(id)

