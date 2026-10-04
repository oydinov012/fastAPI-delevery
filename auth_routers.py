

import stat

from fastapi import APIRouter , status
from fastapi.exceptions import HTTPException
from models import User
from schemas import SignUp
from database import Sessionlocal
from werkzeug.security import generate_password_hash, check_password_hash


auth_router = APIRouter(
    prefix='/auth'
)


@auth_router.get('/')
async def login():
    return {"message":"login sahifasi"}


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