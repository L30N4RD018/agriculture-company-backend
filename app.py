from routes import crops, smallholdings, storages, deliveries, details, users
from controllers.prediction_controller import PredictionController
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

app = FastAPI()

origins = ["*"]

PC = PredictionController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]    
)


@app.get("/")
def read_root():
    return {"200": "Welcome to Agriculture Company API"}


app.include_router(crops.router)


app.include_router(smallholdings.router)


app.include_router(storages.router)


app.include_router(deliveries.router)


app.include_router(details.router)


app.include_router(users.router)


@app.get("/api/make_recomendation", tags=["IA"])
async def make_recomendation():
    return PC.recomendations()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)