from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Multimodal Recipe Bot")

app.include_router(router)


