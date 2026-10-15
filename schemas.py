import json
from re import I
from tkinter import NO
from token import OP

from pydantic import BaseModel, ConfigDict
from typing import Optional
import os
from dotenv import load_dotenv

from database import Base
load_dotenv()

class SignUp(BaseModel):
    id : Optional[int] = None
    username : str
    email : str
    password : str
    is_staff : Optional[bool] = False
    is_active : Optional[bool] = False


    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example":{
                'username':"mohirdev",
                "email":"mohirdev@gmail.com",
                "password":"parol",
                "is_staff":True,
                "is_activr":True
            }
        }
    )




class Settings(BaseModel):
    authjwt_secret_key : str = os.environ["AUTH_JWT_token"]



class Login(BaseModel):
    username_or_pasword : str
    password : str


class OrderModel(BaseModel):
    id : Optional[int] = None
    quantity : int
    order_statuses : Optional[str] = "PENDING"
    user_id : Optional[int] = None
    product_id : Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "exampe":{
                "quantity":3
            }
        }
    )



class OrderStattusModel(BaseModel):
    order_statuses : Optional[str] = "PENDING"

    model_config =ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example":{
                "order_statuses":"PENDING"
            }
        }
    )



class ProductModel(BaseModel):
    id : Optional[int] = None
    name:str
    price : int

    model_config =ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example":{
                "name":"Mahsulot nomi",
                "Price":200
            }
        }
    )
