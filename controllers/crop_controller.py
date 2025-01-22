from logic.storage_decorator import StorageCapacityDecorator
from logic.crop_handler import crop_validation
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from logic.storage import Storage
import mysql.connector as mc
from logic.crop import Crop
import json
import os

MONTHS = { 1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}

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
                value = crop_validation(crop.__dict__(), connection)
                if isinstance(value, dict):
                    raise HTTPException(status_code=400, detail=value)
                if crop.storage_id is not None:
                    cursor.execute(self._querys["SEARCH_STORAGE"], (crop.storage_id,))
                    storage =cursor.fetchone()
                    storg = Storage(*storage)
                    if crop.quantity > storg.max_capacity - storg.current_capacity + crop.quantity:
                        raise HTTPException(status_code=400, detail={"error": "Quantity must be less than the maximum capacity of the storage"})                    
                    try:
                        StorageCapacityDecorator(storg).increase_capacity(crop.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"error": "The capacity of the storage is exceeded"})
                    cursor.execute(self._querys["STORAGE_UPDATE"], storg.__update_tuple__())                    
                cursor.execute(self._querys["CROP_INSERT"], crop.__tuple__())
                connection.commit()
                return JSONResponse(status_code=201, content={"message": "Crop added successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail={"error": "Crop can't be added"})

    
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
                    raise HTTPException(status_code=400, detail={"error": "Invalid Id"})
                cursor.execute(self._querys["SEARCH_CROP"], (id_crop,))
                crop = cursor.fetchone()
                if crop is None:
                    raise HTTPException(status_code=404, detail={"error": "Crop not found"})
                cr = Crop(*(crop[0], crop[1], crop[2], 
                            crop[3].isoformat() if crop[3] is not None else None, 
                            crop[4].isoformat() if crop[4] is not None else None, 
                            crop[5], crop[6], crop[7]))
                cursor.execute(self._querys["SEARCH_STORAGE"], (cr.storage_id,))
                storage = cursor.fetchone()
                if storage is None and cr.storage_id is not None:
                    raise HTTPException(status_code=404, detail={"error": "Storage not found"})
                if storage is not None:
                    storg = Storage(*storage)
                    try:
                        StorageCapacityDecorator(storg).decrease_capacity(cr.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"error": "The capacity of the storage can't be less than 0"})
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
            value = crop_validation(crop.__dict__(), connection)
            if isinstance(value, dict):
                raise HTTPException(status_code=400, detail=value)
            try:                
                # Check if the crop exists in the database
                cursor.execute(self._querys["SEARCH_CROP"], (crop.id,))
                crop_db = cursor.fetchone()
                if crop_db is None:
                    raise HTTPException(status_code=404, detail={"error": "Crop not found"})
                cr = Crop(*(crop_db))
                cursor.execute(self._querys["SEARCH_STORAGE"], (cr.storage_id,))
                old_storage = cursor.fetchone()
                if old_storage is not None:                
                    old_storage = Storage(*old_storage)
                    if crop.quantity > old_storage.max_capacity - old_storage.current_capacity + cr.quantity:
                        raise HTTPException(status_code=400, detail={"error": "Quantity must be less than the avilable capacity of the storage"})                
                # Check if the new storage is different from the old one
                if cr.storage_id != crop.storage_id:
                    cursor.execute(self._querys["SEARCH_STORAGE"], (crop.storage_id,))
                    new_storage = Storage(*cursor.fetchone())
                    try:
                        if old_storage is not None:
                            StorageCapacityDecorator(old_storage).decrease_capacity(cr.quantity)
                        StorageCapacityDecorator(new_storage).increase_capacity(crop.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"error": "Error while changing the storage"})
                    if old_storage is not None:
                        cursor.execute(self._querys["STORAGE_UPDATE"], old_storage.__update_tuple__())
                    cursor.execute(self._querys["STORAGE_UPDATE"], new_storage.__update_tuple__())
                elif cr.quantity != crop.quantity:
                    try:
                        StorageCapacityDecorator(old_storage).decrease_capacity(cr.quantity)
                        StorageCapacityDecorator(old_storage).increase_capacity(crop.quantity)
                    except ValueError:
                        raise HTTPException(status_code=400, detail={"error": "Error while changing the quantity"})
                    cursor.execute(self._querys["STORAGE_UPDATE"], old_storage.__update_tuple__())
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
                    raise HTTPException(status_code=404, detail={"error": "Crop not found"})
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
                    raise HTTPException(status_code=400, detail={"error": "Invalid Id"})
                cursor.execute(self._querys["SEARCH_STORAGE"], (id_storage,))
                storage = cursor.fetchone()
                if storage is None:
                    raise HTTPException(status_code=404, detail={"error": "Storage not found"})
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
                cursor.execute(self._querys["GET_HARVESTED_CROPS"])
                harvested_crops = cursor.fetchall()
                cursor.execute(self._querys["GET_SOWN_CROPS"])
                sown_crops = cursor.fetchall()
                date_details = []
                for month in MONTHS.values():
                    month_details = {
                        'month': month,
                        'sown': 0,
                        'harvested': 0,
                    }                    
                    for crop in sown_crops:                        
                        if crop[3].strftime("%b").upper() == month:
                            month_details['sown'] += 1
                    for crop in harvested_crops:
                        if crop[4].strftime("%b").upper() == month:
                            month_details['harvested'] += 1
                    date_details.append(month_details)
                return JSONResponse(status_code=200, content=date_details)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Can't show crops per month")