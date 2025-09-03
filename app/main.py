from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .common.config import settings
from .routers import health, transactions

app = FastAPI(
    title=settings.title,
    root_path=settings.root_path,
)

app.include_router(health.router)
app.include_router(transactions.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)


@app.get("/")
def root():
    return {"message": "Welcome to the DimDim Transactions API!"}
