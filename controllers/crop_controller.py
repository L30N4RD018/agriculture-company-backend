from logic.state import CropState, SownState, GermidatedState, StoragedState, DeliveringState, DeliveriedState
from logic.storage_decorator import StorageCapacityDecorator
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from logic.storage import Storage
import mysql.connector as mc
from logic.crop import Crop
import json


class CropsController(object):
    def __init__(self):
        self._config = json.load(open('config/users.json'))
        self._querys = json.load(open('config/querys.json'))

    def insert_crop(self, crop: Crop) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if crop.quantity <= 0:
            raise HTTPException(status_code=400, detail="The quantity must be greater than 0")
        if crop.harvest_date is not None and crop.sow_date is not None and crop.sow_date > crop.harvest_date:
            raise HTTPException(status_code=400, detail="The sow date must be less than the harvest date")
        if not isinstance(crop.state, CropState):
            raise HTTPException(status_code=400, detail="The state must be a CropState instance")
        if isinstance(crop.state, GermidatedState) and crop.harvest_date is None:
            raise HTTPException(status_code=400, detail="The harvest date is required for the Germidated state")
        if isinstance(crop.state, StoragedState) and crop.storage_id is None:
            raise HTTPException(status_code=400, detail="The storage id is required for the Storaged state")
        if isinstance(crop.state, SownState) and crop.smallholding_id is None:
            raise HTTPException(status_code=400, detail="The smallholding id is required for the Sown state")
        try:
            cursor.execute(self._querys['SMALLHOLDING_SEARCHONE'], (crop.smallholding_id,))
            smallholding = cursor.fetchone()
            if smallholding is None and crop.smallholding_id is not None:
                raise HTTPException(status_code=404, detail="Smallholding not found") 
            cursor.execute(self._querys['STORAGE_SEARCHONE'], (crop.storage_id,))
            storage = cursor.fetchone()
            if storage is None and crop.storage_id is not None:
                raise HTTPException(status_code=404, detail="Storage not found")            
            if storage is not None:
                storage = Storage(*storage)
                if crop.quantity > storage.max_capacity - storage.current_capacity:
                    raise HTTPException(status_code=400, detail="The quantity exceeds the storage capacity")             
                StorageCapacityDecorator(storage).increase_capacity(crop.quantity)
                cursor.execute(self._querys['STORAGE_UPDATE'], (storage.max_capacity, storage.current_capacity, storage.ubication, storage.equipment, storage.id))
            cursor.execute(self._querys['CROP_INSERT'], crop.__tuple__()[1:])
            connection.commit()
            return JSONResponse(status_code=201, content={"message": "Crop created"})
        except mc.Error as e:
            connection.rollback()            
            raise HTTPException(status_code=500, detail="Internal server error"+str(e))
        finally:
            cursor.close()
            connection.close()
    
    def delete_crop(self, id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if id <= 0:
            raise HTTPException(status_code=400, detail="Crop id must be greater than 0")
        try:
            cursor.execute(self._querys['CROP_SEARCHONE'], (id,))
            crop = cursor.fetchone()
            if crop is None:
                raise HTTPException(status_code=404, detail="Crop not found")
            crop_data = Crop(*crop)
            cursor.execute(self._querys['STORAGE_SEARCHONE'], (crop_data.storage_id,))
            storage = cursor.fetchone()
            if storage is None and crop_data.storage_id is not None:
                raise HTTPException(status_code=404, detail="Storage not found")
            if storage is not None:
                storage = Storage(*storage)
                StorageCapacityDecorator(storage).decrease_capacity(crop_data.quantity)
                cursor.execute(self._querys['STORAGE_UPDATE'], (storage.max_capacity, storage.current_capacity, storage.ubication, storage.equipment, storage.id))
            cursor.execute(self._querys['CROP_DELETE'], (id,))
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Crop deleted"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    def update_crop(self, crop: Crop) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if crop.quantity <= 0:
            raise HTTPException(status_code=400, detail="The quantity must be greater than 0")
        if crop.harvest_date is not None and crop.sow_date is not None and crop.sow_date > crop.harvest_date:
            raise HTTPException(status_code=400, detail="The sow date must be less than the harvest date")
        if not isinstance(crop.state, CropState):
            raise HTTPException(status_code=400, detail="The state must be a CropState instance")
        if isinstance(crop.state, GermidatedState) and crop.harvest_date is None:
            raise HTTPException(status_code=400, detail="The harvest date is required for the Germidated state")
        if isinstance(crop.state, StoragedState) and crop.storage_id is None:
            raise HTTPException(status_code=400, detail="The storage id is required for the Storaged state")
        if isinstance(crop.state, SownState) and crop.smallholding_id is None:
            raise HTTPException(status_code=400, detail="The smallholding id is required for the Sown state")                
        try:
            cursor.execute(self._querys['CROP_SEARCHONE'], (crop.id,)) 
            old_crop = cursor.fetchone()
            if old_crop is None:
                raise HTTPException(status_code=404, detail="Crop not found")
            old_crop = Crop(*old_crop)
            cursor.execute(self._querys['SMALLHOLDING_SEARCHONE'], (crop.smallholding_id,))
            smallholding = cursor.fetchone()
            if smallholding is None and crop.smallholding_id is not None:
                raise HTTPException(status_code=404, detail="Smallholding not found")
            cursor.execute(self._querys['STORAGE_SEARCHONE'], (crop.storage_id,))
            storage = cursor.fetchone()
            if storage is None and crop.storage_id is not None:
                raise HTTPException(status_code=404, detail="Storage not found")
            if storage is not None:            
                storage = Storage(*storage)
                if crop.quantity > storage.max_capacity - storage.current_capacity:
                    raise HTTPException(status_code=400, detail="The quantity exceeds the storage capacity")
                if crop.quantity > old_crop.quantity:
                    StorageCapacityDecorator(storage).increase_capacity(crop.quantity - old_crop.quantity) 
                else:
                    StorageCapacityDecorator(storage).decrease_capacity(old_crop.quantity - crop.quantity)
                cursor.execute(self._querys['STORAGE_UPDATE'], (storage.__tuple__()))
            cursor.execute(self._querys['CROP_UPDATE'], crop.__tuple__()[1:])
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Crop updated"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()

    def show_crops(self) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(self._querys['CROP_SEARCHALL'])
            crops = cursor.fetchall()
            if crops is None:
                raise HTTPException(status_code=404, detail="Crops not found")
            crops = [Crop(*crop).__dict__() for crop in crops]
            return JSONResponse(status_code=200, content=crops)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def search_crop(self, id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if id <= 0:
            raise HTTPException(status_code=400, detail="Crop id must be greater than 0")
        try:
            cursor.execute(self._querys['CROP_SEARCHONE'], (id,))
            crop = cursor.fetchone()
            if crop is None:
                raise HTTPException(status_code=404, detail="Crop not found")
            crop = Crop(*crop).__dict__()
            return JSONResponse(status_code=200, content=crop)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def show_crops_by_smallholding(self, smallholding_id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if smallholding_id <= 0:
            raise HTTPException(status_code=400, detail="Smallholding id must be greater than 0")
        try:
            cursor.execute(self._querys['SMALLHOLDING_SEARCHONE'], (smallholding_id,))
            smallholding = cursor.fetchall()
            if smallholding is None:
                raise HTTPException(status_code=404, detail="Smallholding not found")
            cursor.execute(self._querys['CROP_SEARCHBY_SMALLHOLDING'], (smallholding_id,))
            crops = cursor.fetchall()
            if crops is None:
                raise HTTPException(status_code=404, detail="Crops not found")
            crops = [Crop(*crop).__dict__() for crop in crops] 
            return JSONResponse(status_code=200, content=crops)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()

    def show_crops_by_storage(self, storage_id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if storage_id <= 0:
            raise HTTPException(status_code=400, detail="Storage id must be greater than 0")
        try:
            cursor.execute(self._querys['STORAGE_SEARCHONE'], (storage_id,))
            storage = cursor.fetchall()
            if storage is None:
                raise HTTPException(status_code=404, detail="Storage not found")
            cursor.execute(self._querys['CROP_SEARCHBY_STORAGE'], (storage_id,))
            crops = cursor.fetchall()
            if crops is None:
                raise HTTPException(status_code=404, detail="Crops not found")
            crops = [Crop(*crop).__dict__() for crop in crops] 
            return JSONResponse(status_code=200, content=crops)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def show_crops_by_date(self) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(self._querys["CROP_GROUPBY_DATE"])
            details = cursor.fetchall()
            if details is None:
                raise HTTPException(status_code=404, detail="Crops not found")
            date_details = [{"year": detail[0], "month": detail[1], "value": detail[2]} for detail in details]
            return JSONResponse(status_code=200, content=date_details)
        except mc.Error:            
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()