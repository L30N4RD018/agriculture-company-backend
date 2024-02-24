from controllers.crop_controller import CropsController
from logic.smallholding import Smallholding
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import mysql.connector as mc
import json

CC = CropsController()

class SmallholdingsController(object):
    def __init__(self):
        self._config = json.load(open('config/users.json'))
        self._querys = json.load(open('config/querys.json'))
    
    def insert_smallholding(self, smallholding: Smallholding) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:

            cursor.execute(self._querys['SMALLHOLDING_INSERT'], smallholding.__tuple__()[1:])            
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Smallholding added successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()

    def delete_smallholding(self, id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if id <= 0:
            raise HTTPException(status_code=400, detail="Smallholding id must be greater than 0")
        if CC.show_smallholding_crops(id).status_code == 200:
            raise HTTPException(status_code=409, detail="Smallholding has crops")
        try:
            cursor.execute(self._querys['SMALLHOLDING_SEARCHONE'], (id,)) 
            smallholding = cursor.fetchone()
            if smallholding is None:
                raise HTTPException(status_code=404, detail="Smallholding not found")
            cursor.execute(self._querys['SMALLHOLDING_DELETE'], (id,))
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Smallholding deleted successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def update_smallholding(self, smallholding: Smallholding) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if smallholding.id <= 0:
            raise HTTPException(status_code=400, detail="Smallholding id must be greater than 0")
        try:
            cursor.execute(self._querys['SMALLHOLDING_SEARCHONE'], (smallholding.id,))
            smallholding_data = cursor.fetchone()
            if smallholding_data is None:
                raise HTTPException(status_code=400, detail="Smallholding not found")

            cursor.execute(self._querys['SMALLHOLDING_UPDATE'], smallholding.__tuple__()[1:])
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Smallholding updated successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def show_smallholdings(self) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(self._querys['SMALLHOLDING_SEARCHALL'])
            smallholdings = cursor.fetchall()
            if smallholdings is None:
                raise HTTPException(status_code=406, detail="Smallholdings not found in database")
            if len(smallholdings) == 0:
                raise HTTPException(status_code=404, detail="Smallholdings not have content")
            smallholdings = [Smallholding(*smallholding).__dict__() for smallholding in smallholdings]
            return JSONResponse(status_code=200, content=smallholdings)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def search_smallholding(self, id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if Smallholding is None:
            raise HTTPException(status_code=400, detail="Smallholding not found")
        try:
            cursor.execute(self._querys['SMALLHOLDING_SEARCHONE'], (id,))
            smallholding = cursor.fetchone()
            smallholding = Smallholding(*smallholding).__dict__()
            return JSONResponse(status_code=200, content=smallholding)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")        
        finally:
            cursor.close()
            connection.close()