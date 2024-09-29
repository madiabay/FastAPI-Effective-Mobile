from fastapi import FastAPI

from code import database
from .products import routers as product_routers
from .orders import routers as order_routers

app = FastAPI()
app.include_router(product_routers.router)
app.include_router(order_routers.router)
app.state.database = database.database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
