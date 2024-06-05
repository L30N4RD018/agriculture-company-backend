from logic.smallholding import Smallholding
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import mysql.connector as mc
import json
import os

class SmallholdingController(object):
    def __init__(self):
        self._querys = json.load(open('config/querys.json'))

    def add_smallholding(self, smallholding: Smallholding) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SMALLHOLDING_INSERT"], smallholding.__tuple__())
                connection.commit()
                return JSONResponse(status_code=201, content={"message": "Smallholding added successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Smallholding can't be added")
            
    
    def delete_smallholding(self, id_smallholding: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                if id_smallholding <= 0 or id_smallholding is None:
                    raise HTTPException(status_code=400, detail=f"Error: Invalid id")
                if self.show_smallholding_crops(id_smallholding).status_code == 200:
                    raise HTTPException(status_code=400, detail=f"Error: Smallholding has crops")
                cursor.execute(self._querys["SEARCH_SMALLHOLDING"], (id_smallholding,))
                smallholding = cursor.fetchone()
                if smallholding is None:
                    raise HTTPException(status_code=404, detail=f"Error: Smallholding not found")
                cursor.execute(self._querys["SMALLHOLDING_DELETE"], (id_smallholding,))
                connection.commit()
                return JSONResponse(status_code=200, content={"message": "Smallholding deleted successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Smallholding can't be deleted -")
    

    def update_smallholding(self, smallholding: Smallholding) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                if smallholding.id <= 0 or smallholding.id is None:
                    raise HTTPException(status_code=400, detail=f"Error: Invalid id")

                cursor.execute(self._querys["SEARCH_SMALLHOLDING"], (smallholding.id,))
                smallholding_db = cursor.fetchone()
                if smallholding_db is None:
                    raise HTTPException(status_code=404, detail=f"Error: Smallholding not found")

                cursor.execute(self._querys["SMALLHOLDING_UPDATE"], smallholding.__update_tuple__())
                connection.commit()            
                return JSONResponse(status_code=200, content={"message": "Smallholding updated successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Smallholding can't be updated")

    
    def show_smallholdings(self) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SHOW_SMALLHOLDINGS"])
                smallholdings = cursor.fetchall()
                if len(smallholdings) == 0:
                    raise HTTPException(status_code=404, detail=f"Error: Smallholdings not found")
                smallholdings = [Smallholding(*smallholding).__dict__() for smallholding in smallholdings]
                return JSONResponse(status_code=200, content=smallholdings)
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't show smallholdings ")

    
    def search_smallholding(self, id_smallholding: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                if id_smallholding <= 0 or id_smallholding is None:
                    raise HTTPException(status_code=400, detail=f"Error: Invalid id")
                cursor.execute(self._querys["SEARCH_SMALLHOLDING"], (id_smallholding,))
                smallholding = cursor.fetchone()
                if smallholding is None:
                    raise HTTPException(status_code=404, detail=f"Error: Smallholding not found")
                smallholding = Smallholding(*smallholding).__dict__()
                return JSONResponse(status_code=200, content=smallholding)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Can't show smallholding")            
            
    def show_smallholding_crops(self, id_smallholding: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                if id_smallholding <= 0 or id_smallholding is None:
                    raise HTTPException(status_code=400, detail=f"Error: Invalid id")
                cursor.execute(self._querys["SHOW_SMALLHOLDING_CROPS"], (id_smallholding,))
                crops = cursor.fetchall()                
                crops = [{
                    "id": crop[0],
                    "type": crop[1],
                    "state": crop[2],
                    "sow_date": crop[3].isoformat() if crop[3] is not None else None,
                    "harvest_date": crop[4].isoformat() if crop[4] is not None else None,
                    "storage_id": crop[5],
                    "smallholding_id": crop[6],
                    "quantity": crop[7]
                
                } for crop in crops]
                return JSONResponse(status_code=200, content=crops)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Can't show smallholding crops")
