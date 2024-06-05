from controllers.delivery_controller import DeliveryController
from fastapi import APIRouter, Depends
from pydantic import BaseModel


router = APIRouter()
DC = DeliveryController()
TAGS = ["Details"]


class DetailModel(BaseModel):
    id: int
    crop_id: int
    quantity: int


@router.get("/api/detials", tags=TAGS)
async def show_details():
    return DC.show_all_delivery_details()


@router.get("/api/details/{id}", tags=TAGS, response_model=DetailModel)
async def search_detail(id: int):
    return DC.show_delivery_details(id)


@router.post("/api/details", tags=TAGS, response_model=DetailModel)
async def add_detail(detail_model: DetailModel):
    return DC.delivery_detail(detail_model.crop_id, detail_model.quantity)


@router.delete("/api/details/{id}", tags=TAGS, response_model=DetailModel)
async def delete_detail(id: int):
    return DC.delete_delivery_detail(id)




