from controllers.smallholding_controller import SmallholdingController
from logic.smallholding import Smallholding
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()
SC = SmallholdingController()
TAGS = ["Smallholdings"]

class SmallholdingModel(BaseModel):
    id: int = None
    size: float
    ubication: str
    shape: str
    delimited: bool

@router.get("/api/smallholdings", tags=TAGS)
async def smallholdings():
    return SC.show_smallholdings()

@router.get("/api/smallholdings/crops/{id}", tags=TAGS, response_model=SmallholdingModel)
async def show_smallholding_crops(id: int):
    return SC.show_smallholding_crops(id)

@router.get("/api/mallholdings/{id}", tags=TAGS, response_model=SmallholdingModel)
async def search_smallholding(id: int):
    return SC.search_smallholding(id)

@router.post("/api/smallholdings", tags=TAGS, response_model=SmallholdingModel)
async def add_smallholding(SmallholdingModel: SmallholdingModel):    
    return SC.add_smallholding(Smallholding(**SmallholdingModel.model_dump()))

@router.put("/api/smallholdings", tags=TAGS, response_model=SmallholdingModel)
async def update_smallholding(SmallholdingModel: SmallholdingModel):
    return SC.update_smallholding(Smallholding(**SmallholdingModel.model_dump()))

@router.delete("/api/smallholdings/{id}", tags=TAGS, response_model=SmallholdingModel)
async def delete_smallholding(id: int):
    return SC.delete_smallholding(id)

