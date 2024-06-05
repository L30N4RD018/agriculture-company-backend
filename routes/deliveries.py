from controllers.delivery_controller import DeliveryController
from fastapi import APIRouter, Depends
from logic.delivery import Delivery
from pydantic import BaseModel
from datetime import date


router = APIRouter()
DC = DeliveryController()
TAGS = ["Deliveries"]


class DeliveryModel(BaseModel):
    id: int
    client_name: str
    deliver_date: date
    request_date: date


@router.get("/api/deliveries", tags=TAGS)
async def show_deliveries():
    return DC.show_deliveries()


@router.get("/api/deliveries/months", tags=TAGS)
async def show_delivery_per_month():
    return DC.show_delivery_month()


@router.get("/api/deliveries/{id}", tags=TAGS, response_model=DeliveryModel)
async def search_delivery(id: int):
    return DC.search_delivery(id)


@router.post("/api/deliveries", tags=TAGS, response_model=DeliveryModel)
async def add_delivery(delivery_model: DeliveryModel):
    return DC.add_delivery(Delivery(**delivery_model.model_dump()))

@router.put("/api/deliveries", tags=TAGS, response_model=DeliveryModel)
async def update_delivery(delivery_model: DeliveryModel):
    return DC.update_delivery(Delivery(**delivery_model.model_dump()))


@router.delete("/api/deliveries/{id}", tags=TAGS, response_model=DeliveryModel)
async def delete_delivery(id: int):
    return DC.delete_delivery(id)

