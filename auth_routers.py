from re import S

from fastapi import APIRouter, Depends , status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from models import User
from sqlalchemy import or_
from schemas import Login, SignUp
from database import Sessionlocal
from async_fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash
auth_router = APIRouter(
    prefix='/auth'
)


@auth_router.get('/')
async def get_salom(autorize : AuthJWT=Depends()):
    try:
        await autorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ro'yxatdan o'ting"
        )
    return "salom sizga xush kelibsiz"


@auth_router.post("/signup")
async def singnup(user : SignUp):


    session = Sessionlocal()
    try:
        username_db = session.query(User).filter(User.username == user.username).first() 
        if username_db is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='bunday username allaachon mavjud')

        email_db = session.query(User).filter(User.email == user.email).first()
        if email_db is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                    detail='email royxatdan utgan'      )

        new_user = User(
            username = user.username,
            email = user.email,
            password = generate_password_hash(user.password),
            is_staff = user.is_staff,
            is_active = user.is_active
            )

        session.add(new_user)
        session.commit()

        data = {
            "success":True,
            "status":201,
            "user":{
                "username":new_user.username,
                "email":new_user.email,
                "is_staff":new_user.is_staff,
                "is_active":new_user.is_active
            },
            "message":"User royxatdan o'tkazildi"
            
        }

        return data
    finally :
        session.close()




@auth_router.post('/login',status_code=200)
async def login(user:Login , autorize:AuthJWT = Depends()):
    sessiya = Sessionlocal()
    try:
        db_user = sessiya.query(User).filter(
            or_(
                User.username == user.username_or_pasword,
                User.email == user.username_or_pasword
            )
        ).first()

        if db_user and check_password_hash(str(db_user.password),user.password): 
            access_token = await autorize.create_access_token(subject=str(db_user.username)) 
            refresh_token = await autorize.create_refresh_token(subject=str(db_user.username)) 

            token = {
                "access":access_token,
                "refresh":refresh_token
            }
            response = {
                "succes":True,
                "code":status.HTTP_200_OK,
                "message":"User muvaffaiyatli login qildi",
                "token":token
            }

            return jsonable_encoder(response)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username yoki parol xato"
            )



    finally :
        sessiya.close()


