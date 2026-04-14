from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from routers import user_router, media_router, review_router

api = FastAPI()  # init FastAPI

api.include_router(user_router)
api.include_router(media_router)
api.include_router(review_router)


@api.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_: Request, exc: RequestValidationError):
	return JSONResponse(
		status_code=422,
		content={
			"detail": "Invalid request payload",
			"errors": exc.errors(),
		},
	)


@api.exception_handler(IntegrityError)
async def integrity_exception_handler(_: Request, exc: IntegrityError):
	return JSONResponse(
		status_code=409,
		content={
			"detail": "Request violates database constraints",
			"error": str(exc.orig),
		},
	)

