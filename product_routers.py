from fastapi import APIRouter , Depends , status
from fastapi.background import P
from fastapi.encoders import jsonable_encoder
from async_fastapi_jwt_auth import AuthJWT
from models import Product, User , Order
from schemas import ProductModel , ProductUpdateModel
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


@product_router.get('/list')
async def product_list_All(authorize:AuthJWT = Depends()):
    try:
        await authorize.jwt_required()
        current_user =  await authorize.get_jwt_subject()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nomalum sahifa"
        )

    sessiya = Sessionlocal()
    try:
        user = sessiya.query(User).filter(User.username == current_user).first()
        assert user is not None
        if user.is_staff : # type: ignore
            
            pruducts = sessiya.query(Product).all()
            if pruducts:
                respons = [
                    {
                        "product_id":product.id,
                        "Product_name":product.name,
                        "price":product.price,

                    } for product in pruducts
                ]
                return jsonable_encoder(
                    {
                        'SUCCESS':True,
                        "message":"Barcha mahsulotlar royxati",
                        "Mahsulotlar":[respons]
                    }
                )
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Mahsulotlar mavjud emas')

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Sizda ruxsat yuq'
            )

    finally :
        sessiya.close()
         

@product_router.delete('/{id}/delete')
async def product_delete(id:int, authorize : AuthJWT = Depends()):
    try:
        await authorize.jwt_required()
        current_user =  await authorize.get_jwt_subject()
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
            pruducts = sessiya.query(Product).filter(Product.id == id).first()
            if pruducts:
                sessiya.delete(pruducts)
                sessiya.commit()
                return jsonable_encoder(
                    {
                        "succes":True,
                        "message":f"Mahsulot [--{pruducts.name} --] bazadan olib tashlandi"
                    }
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,detail="Mahsulot topilmadi"
                )
            
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Sizda ruxsat yuq'
            )

    finally:
        sessiya.close()
                

@product_router.put('/{id}/update')
async def update_product(id:int, new_product:ProductUpdateModel , authorize:AuthJWT = Depends()):
    print("\n\n salom ")
    try:
        await authorize.jwt_required()
        current_user =  await authorize.get_jwt_subject()
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
            product = sessiya.query(Product).filter(Product.id == id).first()
            
            if product:
                old = {"product_id":product.id,
                        "product nomi ":product.name,
                        "avvalgi narx":product.price}
                for key, value in new_product.model_dump(exclude_unset=True).items():
                    setattr(product,key, value)

                
                sessiya.commit()
                return jsonable_encoder(
                    {
                        "succes":True,
                        "message":"Mahsulot malumotlari yangilandi",
                        "product":[
                            {"oldingi_product":old,
                            "yangilangan_mahsulot":
                                {"product_id":product.id,
                                "product nomi ":new_product.name,
                                "avvalgi narx":new_product.price}
                                },
                        ]
                    }
                )
                # sessiya.refresh(product)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,detail="Mahsulot topilmadi"
                )
            
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Sizda ruxsat yuq'
            )

    finally:
        sessiya.close()

































