from logic.delivery import Delivery
import mysql.connector as mc
import json
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import os


class DeliveryController(object):
    def __init__(self):
        self._querys = json.load(open('config/querys.json'))

    def show_deliveries(self) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SHOW_DELIVERIES"])
                deliveries = cursor.fetchall()
                if len(deliveries) == 0:
                    return JSONResponse(status_code=404, content={"message": "Deliveries not found"})
                deliveries = [Delivery(*delivery).__dict__() for delivery in deliveries]
                return JSONResponse(status_code=200, content=deliveries)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Can't show deliveries")
            

    def add_delivery(self, delivery: Delivery) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["DELIVERY_INSERT"], delivery.__tuple__())
                connection.commit()
                delivery_id = cursor.lastrowid
                return JSONResponse(status_code=201, content={"message": "Delivery added successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't add delivery")


    def update_delivery(self, delivery: Delivery) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["DELIVERY_UPDATE"], delivery.__update_tuple__())
                connection.commit()
                return JSONResponse(status_code=200, content={"message": "Delivery updated successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't update delivery")
            

    def delete_delivery(self, id_delivery: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SEARCH_DELIVERY"], (id_delivery,))
                delivery = cursor.fetchone()
                if delivery is None:
                    return JSONResponse(status_code=404, content={"message": "Delivery not found"})
                cursor.execute(self._querys["DELIVERY_DELETE"], (id_delivery,))
                connection.commit()
                return JSONResponse(status_code=200, content={"message": "Delivery deleted successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't delete delivery")


    def search_delivery(self, id_delivery: int) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SEARCH_DELIVERY"], (id_delivery,))
                delivery = cursor.fetchone()
                if delivery is None:
                    return JSONResponse(status_code=404, content={"message": "Delivery not found"})
                delivery = Delivery(*delivery).__dict__()
                return JSONResponse(status_code=200, content=delivery)
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't search delivery")


    def show_all_delivery_details(self):
       with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SHOW_ALL_DETAILS"])
                details = cursor.fetchall()
                if len(details) == 0:
                    return JSONResponse(status_code=404, content={"message": "Details not found"})
                details = [
                    {
                        "detail_id": detail[0],
                        "delivery_id": detail[1],
                        "crop_id": detail[2],
                        "quantity": detail[3],
                        "crop_name": detail[4]
                    }
                    for detail in details]
                return JSONResponse(status_code=200, content=details)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Can't show delivery details")
            

    def delivery_detail(self, id_delivery: int, crop_id: int, quantity) -> JSONResponse:
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SEARCH_DELIVERY"], (id_delivery,))
                delivery = cursor.fetchone()
                if delivery is None:
                    return JSONResponse(status_code=404, content={"message": "Delivery not found"})
                cursor.execute(self._querys["SEARCH_CROP"], (crop_id,))
                crop = cursor.fetchone()
                if crop is None:
                    return JSONResponse(status_code=404, content={"message": "Crop not found"})
                else:
                    if crop[4] != "Storaged":
                        return JSONResponse(status_code=400, content={"message": "Crop not storaged"})
                    if crop[7] < quantity:
                        return JSONResponse(status_code=400, content={"message": "Quantity not available"})
                    else:
                        cursor.execute(self._querys["CROP_UPDATE_QUANTITY"], (crop[7] - quantity, crop_id))
                        cursor.execute(self._querys["INSERT_DETAIL"], (id_delivery, crop_id, quantity, crop[1]))
                        connection.commit()                                         
                        return JSONResponse(status_code=201, content={"message": "Delivery detail added successfully"})                 
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't add delivery detail")


    def show_delivery_details(self, id_delivery):
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SEARCH_DELIVERY"], (id_delivery,))
                delivery = cursor.fetchone()
                if delivery is None:
                    return JSONResponse(status_code=404, content={"message": "Delivery not found"})
                cursor.execute(self._querys["SHOW_DETAILS"], (id_delivery,))
                details = cursor.fetchall()
                if len(details) == 0:
                    return JSONResponse(status_code=404, content={"message": "Details not found"})
                details = [
                    {
                        "detail_id": detail[0],
                        "id_delivery": detail[1],
                        "crop_id": detail[2],
                        "quantity": detail[3]
                    }
                    for detail in details]
                return JSONResponse(status_code=200, content=details)
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't show delivery details")
        

    def delete_delivery_detail(self, id_detail):
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SEARCH_DETAIL"], (id_detail,))
                detail = cursor.fetchone()
                if detail is None:
                    return JSONResponse(status_code=404, content={"message": "Detail not found"})
                cursor.execute(self._querys["SEARCH_CROP"], (detail[2],))
                crop = cursor.fetchone()
                cursor.execute(self._querys["CROP_UPDATE_QUANTITY"], (crop[7] + detail[3], crop[0]))
                cursor.execute(self._querys["DELETE_DETAIL"], (detail[0],))
                connection.commit()
                return JSONResponse(status_code=204, content={"message": "Detail deleted successfully"})                            
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Can't delete detail ")
    
    def show_delivery_month(self):
        with mc.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SHOW_DELIVERY_MONTH"])
                details = cursor.fetchall()
                if details is None:
                    return JSONResponse(status_code=404, content={"message": "Any delivery found"})
                date_details = []
                for detail in details:
                    temp = {'date': f"{detail[0]}-{detail[1]}", 'value': detail[2]}
                    date_details.append(temp)
                return JSONResponse(status_code=200, content=date_details)
            except mc.Error:
                raise HTTPException(status_code=400, detail=f"Error: Can't show delivery per month")
