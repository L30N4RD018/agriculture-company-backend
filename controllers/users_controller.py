from fastapi.responses import JSONResponse
from fastapi import HTTPException
import mysql.connector as mc
import json

class UsersController(object):
    def __init__(self):
        self._config = json.load(open('config/users.json'))
        self._querys = json.load(open('config/querys.json'))
    
    def insert_user(self, email: str = None, rol: str = None) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if email is None or rol is None:
            raise HTTPException(status_code=400, detail="Email and role are required")
        if rol.capitalize() not in ('Admin', 'Manager', 'Employee'):
            raise HTTPException(status_code=400, detail="Invalid role")            
        try:
            cursor.execute(self._querys['USER_INSERT'], (email, rol))
            connection.commit()
            return JSONResponse(status_code=201, content={"message": "User added successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def delete_user(self, email: str = None) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if email is None:
            raise HTTPException(status_code=400, detail="Email is required")
        try:
            cursor.execute(self._querys['USER_SEARCHONE'], (email,))
            user = cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            cursor.execute(self._querys['USER_DELETE'], (email,))
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "User deleted successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def update_user(self, email: str = None, rol: str = None) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if email is None or rol is None:
            raise HTTPException(status_code=400, detail="Email and role are required")
        if rol.capitalize() not in ('Admin', 'Manager', 'Employee'):
            raise HTTPException(status_code=400, detail="Invalid role")
        try:
            cursor.execute(self._querys['USER_SEARCHONE'], (email,))
            user = cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            cursor.execute(self._querys['USER_UPDATE'], (email, rol))
            connection.commit()
            return JSONResponse(status_code=200, content={"message": "User updated successfully"})
        except mc.Error:
            connection.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def search_user(self, email: str = None) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        if email is None:
            raise HTTPException(status_code=400, detail="Email is required")
        try:
            cursor.execute(self._querys['USER_SEARCHONE'], (email,))
            user = cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"rol": user[2]})
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
    
    def show_users(self) -> JSONResponse | HTTPException:
        connection = mc.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(self._querys['USER_SEARCHALL'])
            users = cursor.fetchall()
            if users is None:
                raise HTTPException(status_code=404, detail="Users not found")
            users = [{'id': user[0], 'email': user[1], 'rol': user[2]} for user in users]            
            return JSONResponse(status_code=200, content=users)
        except mc.Error:
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            cursor.close()
            connection.close()
