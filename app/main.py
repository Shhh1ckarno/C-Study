from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router
from app.pages.router import router as pages_router
app=FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(pages_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory="app/templates")