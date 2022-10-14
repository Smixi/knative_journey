from fastapi import FastAPI

from .user_router import router

app = FastAPI()
app.include_router(router)
