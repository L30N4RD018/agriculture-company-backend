from fastapi.responses import JSONResponse
from fastapi import HTTPException
from logic.storage import Storage
import mysql.connector as mc
import json
import os

class StorageController(object):
    def __init__(self):
        self._querys = json.load(open('config/querys.json'))

    def show_storages(self) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SHOW_STORAGES"])
                storages = cursor.fetchall()
                if len(storages) == 0:
                    raise HTTPException(status_code=400, detail={"message": "Storages not found"})
                storages = [Storage(*storage).__dict__() for storage in storages]
                return JSONResponse(status_code=200, content=storages)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"message: Can't show storages")
            finally:
                cursor.close()
                connection.close()

    def add_storage(self, storage: Storage) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                if storage.current_capacity < 0 or storage.max_capacity < 0:
                    raise HTTPException(status_code=400, detail={"message": "Invalid capacity"})

                if storage.current_capacity > storage.max_capacity:
                    raise HTTPException(status_code=400, detail={"message": "Current capacity can't be greater than max capacity"})
                cursor.execute(self._querys["STORAGE_INSERT"], storage.__tuple__())
                connection.commit()
                storage_id = cursor.lastrowid
                return JSONResponse(status_code=201, content={"message": "Storage added successfully",
                                                            "storage_id": storage_id})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't add storage")
            

    def update_storage(self, storage: Storage) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                if storage.id <= 0:
                    raise HTTPException(status_code=400, detail={"message": "Invalid id"})

                cursor.execute(self._querys["SEARCH_STORAGE"], (storage.id,))
                storg = cursor.fetchone()
                if storg is None:
                    return HTTPException(status_code=404, content={"Error": "Storage not found"})

                if storage.current_capacity < 0 or storage.max_capacity < 0:
                    raise HTTPException(status_code=400, detail={"Error": "Invalid capacity"})

                if storage.current_capacity > storage.max_capacity:
                    raise HTTPException(status_code=400, detail={"Error": "Current capacity can't be greater than max capacity"})

                cursor.execute(self._querys["STORAGE_UPDATE"], storage.__update_tuple__())
                connection.commit()
                return JSONResponse(status_code=200, content={"message": "Storage updated successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't update storage")


    def delete_storage(self, id_storage: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                if id_storage <= 0:
                    raise HTTPException(status_code=400, detail={"Error": "Invalid id"})

                cursor.execute(self._querys["SEARCH_STORAGE"], (id_storage,))
                storage = cursor.fetchone()
                if storage is None:
                    return HTTPException(status_code=404, content={"Error": "Storage not found"})

                if self.show_storage_crops(id_storage).status_code == 200:
                    raise HTTPException(status_code=400, detail={"Error": "Storage has crops"})

                cursor.execute(self._querys["STORAGE_DELETE"], (id_storage,))
                connection.commit()
                return JSONResponse(status_code=200, content={"message": "Storage deleted successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't delete storage")
            

    def search_storage(self, id_storage: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SEARCH_STORAGE"], (id_storage,))
                storage = cursor.fetchone()
                if storage is None:
                    raise HTTPException(status_code=404, detail={"Error": "Storage not found"})
                storage = Storage(*storage).__dict__()
                return JSONResponse(status_code=200, content=storage)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Can't show storage")
    
    def show_storage_crops(self, id_storage: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                if id_storage <= 0 or id_storage is None:
                    raise HTTPException(status_code=400, detail={"Error": "Invalid id"})
                cursor.execute(self._querys["SHOW_STORAGE_CROPS"], (id_storage,))                
                crops = cursor.fetchall()                
                crops = [{
                    "id": crop[0],
                    "type": crop[1],
                    "state": crop[2],
                    "sow_date": crop[3],
                    "harvest_date": crop[4],
                    "storage_id": crop[5],
                    "smallholding_id": crop[6],
                    "quantity": crop[7]
                
                } for crop in crops]
                return JSONResponse(status_code=200, content=crops)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Can't show crops")
            finally:
                cursor.close()
                connection.close()
