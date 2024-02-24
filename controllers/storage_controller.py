from controllers.crop_controller import CropsController
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from logic.storage import Storage
import mysql.connector as mc
import json


CC = CropsController()

class StoragesController(object):
    def __init__(self):
        self._config = json.load(open('config/users.json'))
        self._querys = json.load(open('config/querys.json'))
    
    def insert_storage(self, storage: Storage) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if storage.current_capacity < 0 or storage.max_capacity < 0:
            raise HTTPException(status_code=400, detail="Invalid capacity")
        if storage.current_capacity > storage.max_capacity:
            raise HTTPException(status_code=400, detail="Current capacity must be less than max capacity")             
        try:
            cursor.execute(self._querys['STORAGE_INSERT'], storage.__tuple__()[1:])
            connection.commit()
            return JSONResponse(status_code=201, content={"message": "Storage added successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def delete_storage(self, id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if id <= 0:
            raise HTTPException(status_code=400, detail="Storage id must be greater than 0")        
        try:
            cursor.execute(self._querys['STORAGE_SEARCHONE'], (id,))
            storage = cursor.fetchone()
            if storage is None:
                raise HTTPException(status_code=404, detail="Storage not found")
            if CC.show_crops_by_smallholding(id).status_code == 200:
                raise HTTPException(status_code=400, detail="Storage is being used by a crop")
            cursor.execute(self._querys['STORAGE_DELETE'], (id,))
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Storage deleted successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def update_storage(self, storage: Storage) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if storage.id <= 0:
            raise HTTPException(status_code=400, detail="Storage id must be greater than 0")
        if storage.current_capacity < 0 or storage.max_capacity < 0:
            raise HTTPException(status_code=400, detail="Invalid capacity")
        if storage.current_capacity > storage.max_capacity:
            raise HTTPException(status_code=400, detail="Current capacity must be less than max capacity")
        if storage.crop_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid crop id")
        try:
            cursor.execute(self._querys['STORAGE_SEARCHONE'], (storage.id,))
            storage_data = cursor.fetchone()
            if storage_data is None:
                raise HTTPException(status_code=400, detail="Storage not found")
            cursor.execute(self._querys['STORAGE_UPDATE'], storage.__tuple__()[1:])
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Storage updated successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def show_storages(self) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(self._querys['STORAGE_SEARCHALL'])
            storages = cursor.fetchall()
            if storages is None or len(storages) == 0:
                raise HTTPException(status_code=404, detail="Storages not found")
            storages = [Storage(*storage).__dict__() for storage in storages]
            return JSONResponse(status_code=200, content=storages)        
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def search_storage(self, id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if id <= 0:
            raise HTTPException(status_code=400, detail="Storage id must be greater than 0")
        try:
            cursor.execute(self._querys['STORAGE_SEARCHONE'], (id,))
            storage = cursor.fetchone()
            if storage is None or len(storage) == 0:
                raise HTTPException(status_code=404, detail="Storage not found")
            storage = Storage(*storage).__dict__()
            return JSONResponse(status_code=200, content=storage)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()