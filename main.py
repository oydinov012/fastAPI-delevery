from fastapi import FastAPI

import auth_routers
import orders_routers
from schemas import Settings
from async_fastapi_jwt_auth import AuthJWT

@AuthJWT.load_config # type: ignore
def get_config():
    return Settings()

app = FastAPI()
app.include_router(orders_routers.order_router)
app.include_router(auth_routers.auth_router)

@app.get('/')
async def salom():
    return {
        "message":"FastAPI loyihasiga xush kelibsiz",
        "data":[
            {
                "ism":"kimdir",
                "familiya":"nimadir",
                "email":None
            }
        ]
            }