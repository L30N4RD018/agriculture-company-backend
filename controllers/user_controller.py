from auth0.authentication.database import Database
from fastapi.responses import JSONResponse
from auth0.authentication import GetToken
from auth0.management.users import Users
from auth0.management.roles import Roles
from fastapi import HTTPException
import mysql.connector as mc
import json
import os


AUTH0_DATABASE = Database(os.getenv('AUTH0_DOMAIN'), os.getenv('AUTH0_CLIENT_ID'), os.getenv('AUTH0_CLIENT_SECRET'))
USERS = Users(domain=os.getenv('AUTH0_DOMAIN'), token=os.getenv("AUTH0_API_TOKEN"))
ROLES = Roles(domain=os.getenv('AUTH0_DOMAIN'), token=os.getenv("AUTH0_API_TOKEN"))
GET_TOKEN = GetToken(os.getenv('AUTH0_DOMAIN'), os.getenv('AUTH0_CLIENT_ID'), client_secret=os.getenv('AUTH0_CLIENT_SECRET'))


class UsersController(object):
    def __init__(self):
        self._querys = json.load(open('config/querys.json'))
    

    def show_users(self):
        with mc.connect(
            host=os.getenv('DB_USERS_HOST'),
            user=os.getenv('DB_USERS_USER'),
            password=os.getenv('DB_USERS_PASSWORD'),
            database=os.getenv('DB_USERS_NAME'),
            port = os.getenv('DB_USERS_PORT')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["SHOW_USERS"])
                users = cursor.fetchall()
                return JSONResponse(status_code=200, content=users)
            except mc.Error:
                raise HTTPException(status_code=400, detail="Error: Users can't be showed")

    
    def search_user(self, email: str = None):
        if email is None:
            raise HTTPException(status_code=400, detail={"Error": "Email is required"})
        if '@' not in email or email.split('@')[1] != 'agcompany.com':
            raise HTTPException(status_code=400, detail={"Error": "Email is not valid"})
        try:
            user = ''#USERSBYE.search_users_by_email(email)
            return JSONResponse(status_code=200, content=user)    
        except Exception as e:
            raise HTTPException(status_code=400, detail={"Error": str(e)})                


    def add_user(self,
                  email: str = None,
                  password: str = None,
                  nickname: str = None,
                  name: str = None,
                  picture: str = None,
                  roles: list[str] = None):
        with mc.connect(
            host=os.getenv('DB_USERS_HOST'),
            user=os.getenv('DB_USERS_USER'),
            password=os.getenv('DB_USERS_PASSWORD'),
            database=os.getenv('DB_USERS_NAME'),
            port = os.getenv('DB_USERS_PORT')            
            
        ) as connection, connection.cursor() as cursor:
            if email is None or password is None:
                raise HTTPException(status_code=400, detail={"Error": "Email and password are required"})
            if '@' not in email or email.split('@')[1] != 'agcompany.com':
                raise HTTPException(status_code=400, detail={"Error": "Email is not valid"})
            try:
                cursor.execute(self._querys["SHOW_USER"], (email,))
                old_user = cursor.fetchone()
                if old_user is not None:
                    raise HTTPException(status_code=400, detail={"message": "User already exists"})
                cursor.execute(self._querys["INSERT_USER"], (email, nickname, name, picture))                
                user_id = cursor.lastrowid
                cursor.execute(self._querys["SHOW_ROLES"])
                db_roles = cursor.fetchall()
                if roles is None:
                    raise HTTPException(status_code=400, detail={"Error": "Don't exist roles in the system"})
                roles = [role[0] for role in db_roles if role[1] in roles]                
                for role in roles:
                    cursor.execute(self._querys["INSERT_USER_ROLE"], (user_id, role))
                connection.commit()
                user_sign =AUTH0_DATABASE.signup(email, password,"Username-Password-Authentication", nickname=nickname, name=name, picture=picture)
                if user_sign is None:
                    raise HTTPException(status_code=400, detail={"Error": "User can't be added"})
                sys_roles = ROLES.list()['roles']
                if sys_roles is None:
                    raise HTTPException(status_code=400, detail={"Error": "Don't exist roles in the system"})
                sys_roles = {role['name']: role['id'] for role in sys_roles}                                
                for role in roles:
                    if role not in sys_roles:
                        raise HTTPException(status_code=400, detail={"Error": f"Role {role} don't exist in the system"})
                USERS.add_roles(f"auth0|{user_sign['_id']}", [sys_roles[role] for role in roles])                                
                return JSONResponse(status_code=201, content={"message": "User added successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: User can't be added ")


    def update_user(self, 
                    email: str = None, 
                    nickname: str = None, 
                    name: str = None, 
                    picture: str = None, 
                    roles: list[str] = None):
        with mc.connect(
            host=os.getenv('DB_USERS_HOST'),
            user=os.getenv('DB_USERS_USER'),
            password=os.getenv('DB_USERS_PASSWORD'),
            database=os.getenv('DB_USERS_NAME'),
            port = os.getenv('DB_USERS_PORT')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["UPDATE_USER"], (nickname, name, picture, email))
                connection.commit()
                return JSONResponse(status_code=200, content={"message": "User updated successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: User can't be updated")


    def delete_user(self, email: str = None):
        with mc.connect(
            host=os.getenv('DB_USERS_HOST'),
            user=os.getenv('DB_USERS_USER'),
            password=os.getenv('DB_USERS_PASSWORD'),
            database=os.getenv('DB_USERS_NAME'),
            port = os.getenv('DB_USERS_PORT')
        ) as connection, connection.cursor() as cursor:
            try:
                cursor.execute(self._querys["DELETE_USER"], (email,))
                connection.commit()
                return JSONResponse(status_code=200, content={"message": "User deleted successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: User can't be deleted")
            
    
    def login(self, email: str = None, password: str = None):
        try:            
            token = GET_TOKEN.login(username=email, password=password, 
                                    realm='Username-Password-Authentication', 
                                    scope='openid profile', 
                                    audience=os.getenv('AUTH0_AUDIENCE'))
            if token is None:
                raise HTTPException(status_code=400, detail={"Error": "User or password incorrect"})                                   
            return JSONResponse(status_code=200, content=token)
        except Exception:
            raise HTTPException(status_code=400, detail={"Error": "The user can't be logged in"})
    

    def create_permissions(self, permissions: list[str] = None):
        with mc.connect(
            host=os.getenv('DB_USERS_HOST'),
            user=os.getenv('DB_USERS_USER'),
            password=os.getenv('DB_USERS_PASSWORD'),
            database=os.getenv('DB_USERS_NAME'),
            port = os.getenv('DB_USERS_PORT')
        ) as connection, connection.cursor() as cursor:
            try:
                for permission in permissions:
                    cursor.execute(self._querys["INSERT_PERMISSION"], (permission,))
                connection.commit()
                return JSONResponse(status_code=201, content={"message": "Permissions added successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Permissions can't be added")


    def create_roles(self, roles: list[str] = None):
        with mc.connect(
            host=os.getenv('DB_USERS_HOST'),
            user=os.getenv('DB_USERS_USER'),
            password=os.getenv('DB_USERS_PASSWORD'),
            database=os.getenv('DB_USERS_NAME'),
            port = os.getenv('DB_USERS_PORT')
        ) as connection, connection.cursor() as cursor:
            try:
                for role in roles:
                    cursor.execute(self._querys["INSERT_ROLE"], (role,))
                connection.commit()
                return JSONResponse(status_code=201, content={"message": "Roles added successfully"})
            except mc.Error:
                connection.rollback()
                raise HTTPException(status_code=400, detail=f"Error: Roles can't be added")
        