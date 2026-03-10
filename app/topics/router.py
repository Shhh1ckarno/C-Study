from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_decoded_token, get_current_user_optional
from app.topics.dao import TopicsDAO
from app.users.dependencies import templates

router = APIRouter(prefix="/topics", tags=["Темы"])

@router.post("/delete_topic")
async def delete_topic(
    topic_id: int = Form(...),
    current_user=Depends(get_current_decoded_token)
):
    if not current_user or current_user["role"] != "admin":
        return RedirectResponse(url="/auth", status_code=303)

    await TopicsDAO.delete_by_id(id=topic_id)
    return RedirectResponse(url="/auth", status_code=303)

@router.post("/add_topic")
async def add_topic(title: str = Form(...),
                    description: str = Form(...),
                    tasks_ids: str = Form(...),
                      current_user=Depends(get_current_decoded_token)):
    if not current_user or current_user["role"] != "admin":
        return RedirectResponse(url="/auth", status_code=303)
    tasks_ids_list = [int(id.strip()) for id in tasks_ids.split(",") if id.strip().isdigit()]
    await TopicsDAO.add(title=title, description=description, tasks_ids=tasks_ids_list)
    return RedirectResponse(url="/auth", status_code=303)

@router.get("/{topic_id}", response_class=HTMLResponse, include_in_schema=False)
async def get_topic_page(request: Request, topic_id: int, user=Depends(get_current_user_optional)):
    topic = await TopicsDAO.get_one_or_none(id=topic_id)
    if not topic:
        return RedirectResponse(url="/auth")
    tasks = await TopicsDAO.get_tasks_from_topic(topic_id=topic_id)
    return templates.TemplateResponse("theory.html", {
        "request": request, 
        "user": user,
        "topic": topic,
        "tasks": tasks,
        "first_task_id": tasks[0].id if tasks else None
    })