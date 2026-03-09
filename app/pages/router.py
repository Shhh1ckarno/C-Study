from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.topics.dao import TopicsDAO
from app.users.dependencies import get_current_decoded_token, get_current_user_optional, templates
from app.users.dependencies import get_current_user
router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и регистрация страницы"]
)


@router.get("", response_class=HTMLResponse, include_in_schema=False)
async def get_main_page(request: Request, user=Depends(get_current_user_optional)):

    topics = await TopicsDAO.get_all()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "user": user,
        "topics": topics
    })

@router.get("/register_page", response_class=HTMLResponse, include_in_schema=False)
async def get_register_page(request: Request, email: Optional[str] = None):
    return templates.TemplateResponse("registration.html", {
        "request": request, 
        "email": email
    })

@router.get("/login_page", response_class=HTMLResponse, include_in_schema=False)
async def get_login_page(request: Request, user=Depends(get_current_user_optional), email: Optional[str] = None):
    if user:
        return RedirectResponse(url="/auth")
        
    return templates.TemplateResponse("login.html", {"request": request, "email": email})



