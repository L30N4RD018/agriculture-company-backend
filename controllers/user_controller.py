from auth0.authentication.database import Database
from fastapi.responses import JSONResponse
from auth0.authentication import GetToken
from auth0.management.users import Users
from auth0.management.users_by_email import UsersByEmail
from auth0.management.roles import Roles
from fastapi import HTTPException
import mysql.connector as mc
import json
import os


AUTH0_DATABASE = Database(os.getenv('AUTH0_DOMAIN'), os.getenv('AUTH0_CLIENT_ID'), os.getenv('AUTH0_CLIENT_SECRET'))
GET_TOKEN = GetToken(os.getenv('AUTH0_DOMAIN'), os.getenv('AUTH0_CLIENT_ID'), client_secret=os.getenv('AUTH0_CLIENT_SECRET'))
token = GET_TOKEN.client_credentials(audience=os.getenv('AUTH0_AUDIENCE_SYS'))
USERS = Users(domain=os.getenv('AUTH0_DOMAIN'), token=token['access_token'])
ROLES = Roles(domain=os.getenv('AUTH0_DOMAIN'), token=token['access_token'])


class UsersController(object):
    def __init__(self):
        self._querys = json.load(open('config/querys.json'))
    

    def show_users(self):
        try:
            users = USERS.list()
            users = [{
                'id': user['user_id'],
                'email': user['email'],                
                'name': user['name']                
            } for user in users['users']]
            for user in users:
                roles = USERS.list_roles(user['id'])['roles']
                roles = [role['name'] for role in roles]
                user['roles'] = roles
            return JSONResponse(status_code=200, content=users)
        except:
            raise HTTPException(status_code=400, detail={"error": "Users can't be shown"})

    
    def search_user(self, email: str = None):
        if email is None:
            raise HTTPException(status_code=400, detail={"error": "Email is required"})
        if '@' not in email or email.split('@')[1] != 'agcompany.com':
            raise HTTPException(status_code=400, detail={"error": "Email is not valid"})
        try:
            user = ''
            return JSONResponse(status_code=200, content=user)    
        except Exception as e:
            raise HTTPException(status_code=400, detail={"error": str(e)})                


    def add_user(self,
                  email: str = None,
                  password: str = None,
                  given_name: str = None,
                  family_name: str = None,
                  picture: str = None,
                  roles: list[str] = None,
                  connection: str = 'Username-Password-Authentication'):
        if email is None:
            raise HTTPException(status_code=400, detail={"error": "Email is required"})            
        if '@' not in email or email.split('@')[1] != 'agcompany.com':
            raise HTTPException(status_code=400, detail={"error": "Email is not valid"})
        if password is None:
            raise HTTPException(status_code=400, detail={"error": "Password is required"})            
        try:            
            user = {
                "email": email,
                "password": password,
                "given_name": given_name,
                "family_name": family_name,
                "picture": picture,
                "connection": connection
            }
            user = {key: value for key, value in user.items() if value is not None}
            response = USERS.create(user)            
            roles_info = ROLES.list()['roles']
            roles = [role['id'] for role in roles_info if role['name'] in roles]
            USERS.add_roles(response['user_id'], roles)
            return JSONResponse(status_code=201, content={"message": "User created successfully"})                  
        except:            
            raise HTTPException(status_code=400, detail={"error": f"The user can't be created"})

    def update_user(self, 
                    email: str = None, 
                    nickname: str = None, 
                    name: str = None, 
                    picture: str = None, 
                    roles: list[str] = None):
        pass


    def delete_user(self, id: str = None):
        if id is None:
            raise HTTPException(status_code=400, detail={"error": "Id is required"})
        try:
            USERS.delete(id)
            return JSONResponse(status_code=200, content={"message": "User deleted successfully"})
        except:
            raise HTTPException(status_code=400, detail={"error": "User can't be deleted"})
            
    
    def login(self, email: str = None, password: str = None):
        try:            
            token = GET_TOKEN.login(username=email, password=password, 
                                    realm='Username-Password-Authentication', 
                                    scope='openid profile', 
                                    audience=os.getenv('AUTH0_AUDIENCE'))
            if token is None:
                raise HTTPException(status_code=400, detail={"error": "User or password incorrect"})                                   
            return JSONResponse(status_code=200, content=token)
        except Exception as e:
            raise HTTPException(status_code=400, detail={"error": f"The user can't be logged in {str(e)}"})
    
    
    def show_roles(self):
        try:            
            roles = ROLES.list()            
            return JSONResponse(status_code=200, content=roles['roles'])
        except Exception as e:
            raise HTTPException(status_code=400, detail={"error": f"Roles can't be shown {str(e)}"})            
    
    
    def add_role(self, name: str = None, description: str = None):
        if name is None:
            raise HTTPException(status_code=400, detail={"error": "Name is required"})
        try:
            role = {
                "name": name,
                "description": description
            }
            role = {key: value for key, value in role.items() if value is not None}
            print(role)
            ROLES.create(role)
            return JSONResponse(status_code=201, content={"message": "Role created successfully"})
        except Exception as e:
            print(f'{e}')
            raise HTTPException(status_code=400, detail={"error": f"Role can't be created"})                
    
    
    def delete_role(self, id: str = None):
        if id is None:
            raise HTTPException(status_code=400, detail={"error": "Id is required"})
        try:            
            ROLES.delete(id)
            return JSONResponse(status_code=200, content={"message": "Role deleted successfully"})
        except:
            raise HTTPException(status_code=400, detail={"error": f"Role can't be deleted"})                    