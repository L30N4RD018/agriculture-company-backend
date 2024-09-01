from controllers.user_controller import UsersController
from fastapi import APIRouter, Query
from pydantic import BaseModel


router = APIRouter()
URC = UsersController()
TAGS = ["Users"]


class UserModel(BaseModel):
    id: int = None
    username: str
    password: str
    nickname: str = None
    name: str = None
    picture: str = None
    roles: list[str]


@router.get("/api/users", tags=TAGS)
async def show_users():
    return URC.show_users()


@router.get("/api/users/login", tags=TAGS)
async def login_user(username: str = Query(...), password: str = Query(...)):
    return URC.login(username, password)


@router.post("/api/users", tags=TAGS, response_model=UserModel)
async def add_user(user_model: UserModel):
    return URC.add_user(user_model.username, user_model.password, user_model.nickname, 
                        user_model.name, user_model.picture, user_model.roles) 


@router.post("/api/users/roles", tags=TAGS)
async def create_roles(role: str):
    return URC.create_roles(role)


# @router.get("/api/users/{id}", tags=TAGS)
# async def search_user(id: int):
#     return URC.get_user_rol(id) #Change name of the method


# @router.put("/api/users", tags=TAGS)
# async def update_user(id: int = Query(...), username: str = Query(...), password: str = Query(...), role_id: int = Query(...)):
#     return URC.update_user_rol(id, username, password, role_id) #Change name of the method


# @router.delete("/api/users/{id}", tags=TAGS)
# async def delete_user(id: int):
#     return URC.delete_user_rol(id) #Change name of the method
