from logic.storage_decorator import StorageCapacityDecorator
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from logic.storage import Storage
import mysql.connector as mc
from logic.crop import Crop
import json
import os

class CropValidator:
    @staticmethod
    def validate(crop: Crop, storage: list = None, smallholding: list = None):
        if crop.quantity <= 0:
            raise HTTPException(status_code=400, detail={"message": "Quantity must be greater than 0"})
        if crop.harvest_date is not None and crop.sow_date >= crop.harvest_date:
            raise HTTPException(status_code=400, detail={"message": "Sow date must be less than harvest date"})
        if smallholding is None and crop.smallholding_id is not None:
            raise HTTPException(status_code=404, detail={"message": "Smallholding not found"})                                
        if storage is None and crop.storage_id is not None:
            raise HTTPException(status_code=404, detail={"message": "Storage not found"})

class CropsController(object):
    def __init__(self):
        self._querys = json.load(open('config/querys.json'))

    def add_crop(self, crop: Crop) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SEARCH_SMALLHOLDING"], (crop.smallholding_id,))
                smallholding = cursor.fetchone()
                cursor.execute(self._querys["SEARCH_STORAGE"], (crop.storage_id,))
                storage =cursor.fetchone()
                CropValidator.validate(crop, storage, smallholding)
                if storage is not None:
                    if crop.quantity > storage[1] - storage[2]:
                        raise HTTPException(status_code=400, detail={"message": "Quantity must be less than the maximum capacity of the storage"})
                    storg = Storage(*storage)
                    try:
                        StorageCapacityDecorator(storg).increase_capacity(crop.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"message": "The capacity of the storage is exceeded"})
                    cursor.execute(self._querys["STORAGE_UPDATE"], storg.__update_tuple__())
                cursor.execute(self._querys["CROP_INSERT"], crop.__tuple__())
                connection.commit()
                return JSONResponse(status_code=201, content={"message": "Crop added successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Crop can't be added")
    
    def show_crops(self) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SHOW_CROPS"])
                crops = cursor.fetchall()
                crops = [{
                    'id': crop[0],
                    'type': crop[1],
                    'state': crop[2],
                    'sow_date': crop[3].isoformat() if crop[3] is not None else None,
                    'harvest_date': crop[4].isoformat() if crop[4] is not None else None,
                    'storage_id': crop[5],
                    'smallholding_id': crop[6],
                    'quantity': crop[7]
                } for crop in crops]
                return JSONResponse(status_code=200, content=crops)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Crops can't be shown")        

    def delete_crop(self, id_crop: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:                
                if id_crop <= 0 or id_crop is None:
                    raise HTTPException(status_code=400, detail={"message": "Invalid Id"})
                cursor.execute(self._querys["SEARCH_CROP"], (id_crop,))
                crop = cursor.fetchone()
                if crop is None:
                    raise HTTPException(status_code=404, detail={"message": "Crop not found"})
                cr = Crop(*(crop[0], crop[1], crop[2], 
                            crop[3].isoformat() if crop[3] is not None else None, 
                            crop[4].isoformat() if crop[4] is not None else None, 
                            crop[5], crop[6], crop[7]))
                cursor.execute(self._querys["SEARCH_STORAGE"], (cr.storage_id,))
                storage = cursor.fetchone()
                if storage is None and cr.storage_id is not None:
                    raise HTTPException(status_code=404, detail={"message": "Storage not found"})
                if storage is not None:
                    storg = Storage(*storage)
                    try:
                        StorageCapacityDecorator(storg).decrease_capacity(cr.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"message": "The capacity of the storage can't be less than 0"})
                    cursor.execute(self._querys["STORAGE_UPDATE"], storg.__update_tuple__())
                cursor.execute(self._querys["CROP_DELETE"], (id_crop,))
                connection.commit()
                return JSONResponse(status_code=200, content={"message": "Crop deleted successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Crop can't be deleted")
    
    def update_crop(self, crop: Crop) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SEARCH_CROP"], (crop.id,))
                crop_db = cursor.fetchone()
                if crop_db is None:
                    raise HTTPException(status_code=404, detail={"message": "Crop not exist"})
                crop_db = Crop(*crop_db)
                cursor.execute(self._querys["SEARCH_STORAGE"], (crop.storage_id,))
                storage = cursor.fetchone()
                cursor.execute(self._querys["SEARCH_SMALLHOLDING"], (crop.smallholding_id,))
                smallholding = cursor.fetchone()
                CropValidator.validate(crop, storage, smallholding)
                storage = Storage(*storage)
                if crop.quantity > storage.max_capacity - storage.current_capacity + crop_db.quantity:
                    raise HTTPException(status_code=400, detail={"message": "Quantity must be less than the maximum capacity of the storage"})
                if crop_db.storage_id != crop.storage_id:
                    try:
                        StorageCapacityDecorator(storage).decrease_capacity(crop_db.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"message": "The capacity of the storage can't be less than 0"})
                    cursor.execute(self._querys["STORAGE_UPDATE"], storage.__update_tuple__())
                    cursor.execute(self._querys["SEARCH_STORAGE"], (crop.storage_id,))
                    storage = cursor.fetchone()
                    storage = Storage(*storage)
                    try:
                        StorageCapacityDecorator(storage).increase_capacity(crop.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"message": "The capacity of the storage is exceeded"})
                    cursor.execute(self._querys["STORAGE_UPDATE"], storage.__update_tuple__())                
                if crop_db.quantity != crop.quantity:
                    if crop_db.storage_id is not None and storage.current_capacity == 0:                        
                        raise HTTPException(status_code=400, detail={"message": "This crop it was in a storage and the storage is empty"})
                    try:
                        StorageCapacityDecorator(storage).decrease_capacity(crop_db.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"message": "The capacity of the storage can't be less than 0"})
                    try:
                        StorageCapacityDecorator(storage).increase_capacity(crop.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"message": "The capacity of the storage is exceeded"})
                    cursor.execute(self._querys["STORAGE_UPDATE"], storage.__update_tuple__())
                cursor.execute(self._querys["CROP_UPDATE"], crop.__update_tuple__())
                connection.commit()               
                return JSONResponse(status_code=200, content={"message": "Crop updated successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Crop can't be updated")
    
    def search_crop(self, id_crop: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SEARCH_CROP"], (id_crop,))
                crop = cursor.fetchone()
                if crop is None:
                    raise HTTPException(status_code=404, detail={"message": "Crop not found"})
                crop = {
                    'id': crop[0],
                    'type': crop[1],
                    'state': crop[2],
                    'sow_date': crop[3].isoformat() if crop[3] is not None else None,
                    'harvest_date': crop[4].isoformat() if crop[4] is not None else None,
                    'storage_id': crop[5],
                    'smallholding_id': crop[6],
                    'quantity': crop[7]
                }
                return JSONResponse(status_code=200, content=crop)
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Crop can't be shown")


    def show_storage_crops(self, id_storage: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                if id_storage <= 0:
                    raise HTTPException(status_code=400, detail={"message": "Invalid Id"})
                cursor.execute(self._querys["SEARCH_STORAGE"], (id_storage,))
                storage = cursor.fetchone()
                if storage is None:
                    raise HTTPException(status_code=404, detail={"message": "Storage not found"})
                cursor.execute(
                    self._querys["SHOW_STORAGE_CROPS"], (id_storage,))
                crops = cursor.fetchall()
                if len(crops) == 0:
                    return JSONResponse(status_code=404, content={"message": "Crops not found"})
                crops = [{
                    'id': crop[0],
                    'type': crop[1],
                    'state': crop[2],
                    'sow_date': crop[3].isoformat() if crop[3] is not None else None,
                    'harvest_date': crop[4].isoformat() if crop[4] is not None else None,
                    'storage_id': crop[5],
                    'smallholding_id': crop[6],
                    'quantity': crop[7]
                } for crop in crops]
                return JSONResponse(status_code=200, content=crops)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Crops can't be shown")
    
    def show_crops_month(self):
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SHOW_CROPS_MONTH"])
                details = cursor.fetchall()
                if details is None:
                    return JSONResponse(status_code=404, content={"message": "Any crops found"})
                date_details = []
                for detail in details:
                    temp = {
                        'date': f'{detail[0]}-{detail[1]}',
                        'value': detail[2]
                        }                    
                    date_details.append(temp)
                return JSONResponse(status_code=200, content=date_details)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Can't show crops per month")
