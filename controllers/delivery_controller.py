from fastapi.responses import JSONResponse
from fastapi import HTTPException
from logic.delivery import Delivery
import mysql.connector as mc
import json

class DeliveryController(object):
    def __init__(self):
        self._config = json.load(open('config/users.json'))
        self._querys = json.load(open('config/querys.json'))
    
    def insert_delivery(self, delivery: Delivery) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(self._querys['DELIVERY_INSERT'], delivery.__tuple__()[1:])
            connection.commit()
            return JSONResponse(status_code=201, content={"message": "Delivery added successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def delete_delivery(self, id: int) -> JSONResponse | HTTPException: 
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if id <= 0:
            raise HTTPException(status_code=400, detail="Delivery id must be greater than 0")        
        try:
            cursor.execute(self._querys['DELIVERY_SEARCHONE'], (id,))
            delivery = cursor.fetchone()
            if delivery is None:
                raise HTTPException(status_code=404, detail="Delivery not found")
            cursor.execute(self._querys['DELIVERY_DELETE'], (id,))
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Delivery deleted successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def update_delivery(self, delivery: Delivery) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if delivery.id <= 0:
            raise HTTPException(status_code=400, detail="Delivery id must be greater than 0")
        try:
            cursor.execute(self._querys['DELIVERY_SEARCHONE'], (delivery.id,))
            delivery_data = cursor.fetchone()
            if delivery_data is None:
                raise HTTPException(status_code=400, detail="Delivery not found")
            cursor.execute(self._querys['DELIVERY_UPDATE'], delivery.__tuple__()[1:])
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "Delivery updated successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def show_deliveries(self) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(self._querys['DELIVERY_SEARCHALL'])
            deliveries = cursor.fetchall()
            if deliveries is None:
                raise HTTPException(status_code=404, detail="No deliveries found")
            deliveries = [Delivery(*delivery).__dict__() for delivery in deliveries] 
            return JSONResponse(status_code=200, content=deliveries)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def search_delivery(self, id: int) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if id <= 0:
            raise HTTPException(status_code=400, detail="Delivery id must be greater than 0")
        try:
            cursor.execute(self._querys['DELIVERY_SEARCHONE'], (id,))
            delivery = cursor.fetchone()
            if delivery is None:
                raise HTTPException(status_code=404, detail="Delivery not found")
            delivery = Delivery(*delivery).__dict__()
            return JSONResponse(status_code=200, content=delivery)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def show_deliveries_by_date(self) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(self._querys['DELIVERY_GROUPBY_DATE'])
            date_details = cursor.fetchall()
            if date_details is None:
                raise HTTPException(status_code=404, detail="No deliveries found")
            date_details = [{'year': day[0], 'month': day[1], "value": day[2]} for day in date_details]
            return JSONResponse(status_code=200, content=date_details)
        except mc.Error as e:
            raise HTTPException(status_code=500, detail="Internal server error"+str(e))
        finally:
            cursor.close()
            connection.close()