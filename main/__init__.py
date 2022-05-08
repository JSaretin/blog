from fastapi import  FastAPI
from .router import admin, posts

app = FastAPI(prefix="/api")

app.include_router(admin.router)
app.include_router(posts.router)
