from fastapi import FastAPI
from routers import user_router, media_router, review_router

api = FastAPI()  # init FastAPI

api.include_router(user_router)
api.include_router(media_router)
api.include_router(review_router)
