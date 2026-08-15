from fastapi import FastAPI, APIRouter

app = FastAPI()

# Версия 1
v1_router = APIRouter(prefix="/api/v1", tags=["v1"])

@v1_router.get("/products")
async def get_products_v1():
    return {
        "products": [
        {"id": 1, "name": "Ноутбук", "price": 50000}
        ]
        }

# Версия 2
v2_router = APIRouter(prefix="/api/v2", tags=["v2"])

@v2_router.get("/products")
async def get_products_v2():
    return {
        "products": [
        {"id": 1, "name": "Ноутбук", "price": 50000}
        ],
        "metadata": {
        "total": 1,
        "page": 1,
        "per_page": 10
        }
        }

app.include_router(v1_router)
app.include_router(v2_router)