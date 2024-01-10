import random
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from pm_api.web.api.users.schema import User

router = APIRouter()

fake_items_db = [
    User(id=1, name="John Doe", email="john.doe@gmail.com", is_active=True),
    User(id=2, name="Franck Doe", email="Franck.doe@gmail.com", is_active=True),
    User(id=3, name="Vincent Doe", email="Vincent.doe@gmail.com", is_active=True),
    User(id=4, name="Gregoire Doe", email="Gregoire.doe@gmail.com", is_active=True),
    User(id=5, name="Kevin Doe", email="Kevin.doe@gmail.com", is_active=True),
]


@router.get(
    "/users",
    response_model=list[User],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Items found"}},
)
def get_users() -> list[User]:
    return fake_items_db


@router.get(
    "/user",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_201_CREATED: {"description": "Random item found"}},
)
def get_one_user() -> User:
    rn = random.randint(0, len(fake_items_db) - 1)
    return fake_items_db[rn]


@router.get(
    "/user/{user_id}",
    response_model=User,
    responses={200: {"description": "Item found"}},
)
def show_by_id(user_id: int) -> User:
    user = next((user for user in fake_items_db if user.id == user_id), None)
    if user is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.post(
    "/user",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_201_CREATED: {"description": "Item created"}},
)
def create_user(user: User) -> User:
    user.id = random.randint(0, 1000000)
    fake_items_db.append(user)
    return user


# DEPENDENCY INJECTION IN FASTAPI
async def common_parameters(
    q: str | None = None, skip: int = 0, limit: int = 100
) -> dict[str, str | int | None]:
    return {"q": q, "skip": skip, "limit": limit}


@router.get(
    "/users/query",
    status_code=status.HTTP_200_OK,
)
async def read_query(
    commons: Annotated[dict[str, str | int | None], Depends(common_parameters)]
) -> dict[str, str | int | None]:
    return commons


# API KEYS ROUTE PROTECTION
api_keys = ["akljnv13bvi2vfo0b0bw"]

api_key_header = APIKeyHeader(name="Api-Key")


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


@router.get("/users/protected", dependencies=[Depends(get_api_key)])
async def read_protected() -> dict[str, str]:
    return {"data": "You used a valid API key."}
