from fastapi import APIRouter , Depends , status
from fastapi.encoders import jsonable_encoder
from async_fastapi_jwt_auth import AuthJWT
from models import User , Order
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


@order_router.post('/make',status_code=201)
async def create_order(order:OrderModel, autorize:AuthJWT=Depends()):

    try:
        await autorize.jwt_required()
    except Exception as a:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="foydalanish uchun ro'yxatdan o'ting"
        )

    sessiya = Sessionlocal()
    try:

        user = await autorize.get_jwt_subject()
        currenr_user = sessiya.query(User).filter(User.username == user).first()

        if not currenr_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Foydalanuvchi topilmadi')

        new_order = Order(
            quantity = order.quantity
        )
        new_order.user = currenr_user
        sessiya.add(new_order)
        sessiya.commit()
        sessiya.refresh(new_order)

        responce = {
            "order_id":new_order.id,
            "order_status":new_order.order_statuses.value,
            "user":{
                "id":new_order.user_id,
                "username":new_order.user.username,
                "email":new_order.user.email
            }
            }

        return jsonable_encoder(
            {
                "succes":True,
                "message":"Order created",
                "code":status.HTTP_201_CREATED,
                'order':responce
            }
        )



    except Exception as a:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='malumot mavjud emas')
    finally :
        sessiya.close()



@order_router.get('/list')
async def get_all_order(autorize: AuthJWT = Depends()):
    try:
        await autorize.jwt_required()
        username = await autorize.get_jwt_subject()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tizimga kirish kerak"
        )

    sessiya = Sessionlocal()

    try:
        current_user = (
            sessiya.query(User)
            .filter(User.username == username)
            .first()
        )

        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Foydalanuvchi topilmadi"
            )

        if not current_user.is_staff: # type: ignore
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ruxsat berilmagan"
            )

        orders = sessiya.query(Order).all()

        data = [
            {
                "order_id": order.id,
                "order_user": (
                    order.user.username if order.user else None
                ),
                "order_status": order.order_statuses
            }
            for order in orders
        ]

        return {
            "message": "  Barcha buyurtmalar ro'yxati",
            "data": data
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"Order list xatosi: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Serverda xatolik yuz berdi"
        )

    finally:
        sessiya.close()




@order_router.get('/detail/{id:int}')
async def get_detail(id:int,autorize:AuthJWT=Depends()):
    try:
        await autorize.jwt_required()
        username = await autorize.get_jwt_subject()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='ro\'yxatdan otish kk')


    sessiya = Sessionlocal()

    try:
        
        current_user = (
            sessiya.query(User)
            .filter(User.username == username)
            .first()
        )

        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Foydalanuvchi topilmadi"
            )

        if not current_user.is_staff: # type: ignore

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ruxsat berilmagan"
            )

        order = sessiya.query(Order).filter(Order.id == id).first()
        print('order\n\n',order ,'\n\n')

        assert order is not None
        data = {
                "order_id": order.id,
                "order_user": (
                    order.user.username if order.user else None
                ),
                "order_status": order.order_statuses
            }

        return jsonable_encoder(
            {
                "success":True,
                "message":"Order malumotlari yuklandi",
                'data':data
            }
        )

    except HTTPException as a:
        raise

    except Exception as a:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Server bn muammo'
        ) 

    finally:
        sessiya.close()



@order_router.get('/user-orders')
async def main_order(autorize:AuthJWT=Depends()):
    try:
        await autorize.jwt_required()
        current_user =  await autorize.get_jwt_subject()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ro'yxatdan o'tish talab qilinadi"
        )

    sessiya = Sessionlocal()

    try:
        user = sessiya.query(User).filter(User.username == current_user).first()
        assert user is not None
        orders = sessiya.query(Order).filter(Order.user_id == user.id).all()

        data = [
            {
                "order_id":order.id,
                "order_statuses":order.order_statuses,
                "quantity":order.quantity,
                "product":(
                    order.product if order.product else 'mahsulot endi kiritiladi'
                )
            } for order in orders
        ]
        
        assert user is not None
        response = {
            'user':{
                "username":user.username,
                "first_name":user.email,
                "is_staff":user.is_staff
                
            } ,
            'buyurtmalar':data
        }

        return jsonable_encoder({
            "succes":True,
            "message":f"{user.username}ning barcha buyurtmalari",
            'order':response

        })

    except Exception as e:
        raise 
    
    finally:
        sessiya.close()



@order_router.delete('/user-order-delete/{id:int}')
async def order_delete(id:int, autorize:AuthJWT=Depends()):
    try:
        await autorize.jwt_required()
        current_user =  await autorize.get_jwt_subject()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mumkin emas"
        )

    sessiya = Sessionlocal()

    try:
        order = sessiya.query(Order).filter(Order.id == id).first()
        user = sessiya.query(User).filter(User.username == current_user).first()

        assert order is not None
        assert user is not None
        if order.user_id == user.id: # type: ignore
            sessiya.delete(order)
        else:
            raise 
                        

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server bilan svyaz uzildi "
        )

