from os import name

from fastapi import APIRouter , Depends , status
from fastapi.encoders import jsonable_encoder
from async_fastapi_jwt_auth import AuthJWT
from models import Product, User , Order
from schemas import ProductModel
from database import Sessionlocal
from fastapi.exceptions import HTTPException


product_router = APIRouter(
    prefix='/product'
)



@product_router.post('/create')
async def create_product(product:ProductModel, autorize:AuthJWT=Depends()):
    try:
        await autorize.jwt_required()
        current_user =  await autorize.get_jwt_subject()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nomalum sahifa"
        )

    sessiya = Sessionlocal()
    try:
        user = sessiya.query(User).filter(User.username == current_user).first()
        assert user is not None
        if user.is_staff: # type: ignore
            new_product = Product(
                name = product.name,
                price = product.price
            )
            sessiya.add(new_product)
            sessiya.commit()

            return jsonable_encoder(
                {
                    "succes":True,
                    "message":"product yaratildi",
                    "product":[
                        {
                            "name":new_product.name
                        },
                        {
                            "narxi":new_product.price
                        }
                    ],

                }
            )

        else:
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sizda ruxsat yo'q ")

    finally:
        sessiya.close()