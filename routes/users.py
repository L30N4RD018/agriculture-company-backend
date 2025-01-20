from controllers.user_controller import UsersController
from fastapi import APIRouter, Query
from pydantic import BaseModel


router = APIRouter()
URC = UsersController()
TAGS = ["Users"]


class UserModel(BaseModel):
    id : int | None = None  
    email: str
    password: str
    nickname: str | None = None
    given_name: str = None
    family_name: str = None
    name: str | None = None
    picture: str = None
    roles: list[str] = None

class RoleModel(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None


@router.get("/api/users", tags=TAGS)
async def show_users():
    return URC.show_users()


@router.get("/api/users/login", tags=TAGS)
async def login_user(username: str = Query(...), password: str = Query(...)):
    return URC.login(username, password)


@router.post("/api/users", tags=TAGS, response_model=UserModel)
async def add_user(user_model: UserModel):
    return URC.add_user(user_model.email, user_model.password, user_model.given_name, 
                        user_model.family_name, user_model.picture, user_model.roles)

@router.get("/api/users/roles", tags=TAGS)
async def show_roles():
    return URC.show_roles()

@router.post("/api/users/roles", tags=TAGS)
async def add_role(role: RoleModel):
    return URC.add_role(role.name, role.description)

@router.delete("/api/users/roles", tags=TAGS)
async def delete_role(id: int = Query(...)):
    return URC.delete_role(id)


# @router.get("/api/users/{id}", tags=TAGS)
# async def search_user(id: int):
#     return URC.get_user_rol(id) #Change name of the method


# @router.put("/api/users", tags=TAGS)
# async def update_user(id: int = Query(...), username: str = Query(...), password: str = Query(...), role_id: int = Query(...)):
#     return URC.update_user_rol(id, username, password, role_id) #Change name of the method


# @router.delete("/api/users/{id}", tags=TAGS)
# async def delete_user(id: int):
#     return URC.delete_user_rol(id) #Change name of the method