from typing import Union

from fastapi import FastAPI

from app.api.api_v1.api import router as api_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "NYC TAXI - prediction service"}

app.include_router(api_router, prefix="/api/v1")