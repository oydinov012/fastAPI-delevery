from curses.ascii import HT

from fastapi import APIRouter , Depends , status
from fastapi.encoders import jsonable_encoder
from async_fastapi_jwt_auth import AuthJWT
from models import User, Product , Order
from schemas import OrderModel, OrderStattusModel
from database import Sessionlocal
from fastapi.exceptions import HTTPException



order_router = APIRouter(
    prefix='/order'
)


@order_router.get('/')
async def order(authorize:AuthJWT=Depends()):

    try:
        await authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )


    return {"message":"order sahifasi"}

