from fastapi import FastAPI
import uvicorn
import auth_routers
import orders_routers
import product_routers
from schemas import Settings
from async_fastapi_jwt_auth import AuthJWT
import run

@AuthJWT.load_config # type: ignore
def get_config():
    return Settings()

app = FastAPI()
app.include_router(orders_routers.order_router)
app.include_router(auth_routers.auth_router)
app.include_router(product_routers.product_router)

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



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=run.PORT,
        host=run.HOST,
        reload=run.RELOAD
    )