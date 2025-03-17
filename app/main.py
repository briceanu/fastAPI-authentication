from fastapi import FastAPI
from routes.blog_api import router as blog_routes
from routes.user_api import router as user_routes




app = FastAPI()


app.include_router(blog_routes)
app.include_router(user_routes)
