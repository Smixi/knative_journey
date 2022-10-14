from fastapi import FastAPI
from .mail_router import router
from fastapi_cloudevents import install_fastapi_cloudevents

app = FastAPI()
app = install_fastapi_cloudevents(app)
app.include_router(router)
