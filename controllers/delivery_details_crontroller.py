from logic.delivery_details import DeliveryDetails
from fastapi.responses import JSONResponse
from logic.delivery import Delivery
from fastapi import HTTPException
import mysql.connector as mc
from logic.crop import Crop
import json

class DeliveryDetailsController(object):
    def __init__(self) -> None:
        self._config = json.load(open('config/users.json'))
        self._querys = json.load(open('config/querys.json'))
    
    def insert_delivery_details(self, delivery_details: DeliveryDetails) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()       
        try:
            cursor.execute(self._querys['DELIVERY_SEARCHONE'], (delivery_details.delivery_id,))
            delivery = cursor.fetchone()
            if delivery is None:
                raise HTTPException(status_code=404, detail="Delivery not found")
            cursor.execute(self._querys['CROP_SEARCHONE'], (delivery_details.crop_id,))
            crop = cursor.fetchone()
            if crop is None:
                raise HTTPException(status_code=404, detail="Crop not found")
            crop = Crop(*crop)
            if crop.state != 'Storaged':
                raise HTTPException(status_code=400, detail="Crop is not storaged")
            if crop.quantity < delivery_details.quantity:
                raise HTTPException(status_code=400, detail="Quantity is greater than the available") 
            cursor.execute(self._querys['CROP_QUANTITY_UPDATE'], (crop.quantity - delivery_details.quantity, delivery_details.crop_id)) 
            cursor.execute(self._querys['DELIVERY_DETAILS_INSERT'], (delivery_details.__tuple__()[1:]))
            connection.commit()
            return JSONResponse(status_code=201, content={"message": "Delivery details added successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def delete_delivery_details(self, id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if id <= 0 or id is None:
            raise HTTPException(status_code=400, detail="Delivery details id is invalid")
        try:
            cursor.execute(self._querys['DELIVERY_DETAILS_SEARCHONE'], (id,))
            delivery_details = cursor.fetchone()
            if delivery_details is None:
                raise HTTPException(status_code=404, detail="Delivery details not found")
            delivery_details = DeliveryDetails(*delivery_details) 
            cursor.execute(self._querys['CROP_SEARCHONE'], (delivery_details.crop_id,))
            crop = cursor.fetchone()
            if crop is None:
                raise HTTPException(status_code=404, detail="Crop not found")
            crop = Crop(*crop)
            cursor.execute(self._querys['CROP_QUANTITY_UPDATE'], (crop.quantity + delivery_details.quantity, delivery_details.crop_id))            
            cursor.execute(self._querys['DELIVERY_DETAILS_DELETE'], (id,))
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Delivery details deleted successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")        
        finally:
            cursor.close()
            connection.close()
    
    def show_deliveries_details(self) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(self._querys['DELIVERY_DETAILS_SEARCHALL'])
            deliveries = cursor.fetchall()
            if deliveries is None:
                raise HTTPException(status_code=406, detail="Deliveries not found in database")
            if len(deliveries) == 0:
                raise HTTPException(status_code=404, detail="No deliveries found")            
            deliveries = [Delivery(*delivery).__dict__() for delivery in deliveries] 
            return JSONResponse(status_code=200, content=deliveries)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def search_delivery_details(self, delivery_id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if delivery_id <= 0 or delivery_id is None:
            raise HTTPException(status_code=400, detail="Delivery id is invalid")
        try:
            cursor.execute(self._querys['DELIVERY_SEARCHONE'], (delivery_id,))
            delivery = cursor.fetchone()
            if delivery is None:
                raise HTTPException(status_code=404, detail="Delivery not found")
            cursor.execute(self._querys['DELIVERY_DETAILS_SEARCHONE'], (delivery_id,))
            delivery_details = cursor.fetchall()
            if delivery_details is None or len(delivery_details) == 0:
                raise HTTPException(status_code=404, detail="Delivery details not found")            
            delivery_details = DeliveryDetails(*delivery_details).__dict__()
            return JSONResponse(status_code=200, content=delivery_details)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()