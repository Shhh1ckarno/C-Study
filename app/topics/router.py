from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from app.users.dependencies import get_current_decoded_token
from app.topics.dao import TopicsDAO

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