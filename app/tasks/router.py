from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.tasks.dao import TasksDAO
from app.tasks.schemas import STaskCreate, TaskAnswersSchema
from app.topics.dao import TopicsDAO
from app.users.dependencies import get_current_decoded_token
from app.users.dependencies import templates

router = APIRouter(prefix="/tasks", tags=["Задачи"])

@router.post("/create")
async def create_task(
    title: str = Form(...),
    description: str = Form(None),
    raw_answers: str = Form(..., alias="answers"), 
    raw_correct: str = Form(..., alias="correct_answers"), 
    decoded_token: dict = Depends(get_current_decoded_token)
):
    if decoded_token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    try:
        ans_list = [a.strip() for a in raw_answers.split(",")]
        corr_list = [int(c.strip()) for c in raw_correct.split(",")]
        
        answers_obj = TaskAnswersSchema(answers=ans_list, correct_answers=corr_list)
        
        task_data = STaskCreate(
            title=title,
            description=description,
            answers=answers_obj
        )
        await TasksDAO.add_task(task_data)
        return RedirectResponse(url="/auth", status_code=303)
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка сервера при создании задачи")

@router.post("/delete")
async def delete_task(task_id: int = Form(...), decoded_token: dict = Depends(get_current_decoded_token)):
    if decoded_token["role"] != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления задачи")
    await TasksDAO.delete_by_id(task_id)
    return RedirectResponse(url="/auth", status_code=303)

@router.post("/tasks_into_topic")
async def tasks_into_topic(task_id: int = Form(...), 
                          topic_id: int = Form(...),
                          decoded_token: dict = Depends(get_current_decoded_token)):
    if decoded_token["role"] != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав для добавления задачи в тему")
    await TopicsDAO.add_task_into_topic(task_id=task_id, topic_id=topic_id)
    return RedirectResponse(url="/auth", status_code=303)

@router.get("/{task_id}")
async def get_task_page(request: Request, task_id: int, user=Depends(get_current_decoded_token)):
    task = await TasksDAO.get_one_or_none(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # Находим тему (она находится, судя по логам)
    topic = await TopicsDAO.find_topics_by_task(task_id=task_id)
    
    navigation_tasks = []
    if topic:
        # Загружаем список задач
        navigation_tasks = await TopicsDAO.get_tasks_from_topic(topic_id=topic.id)
    
    return templates.TemplateResponse("practice.html", {
        "request": request,
        "task": task,
        "user": user,
        "topic": topic,
        "navigation_tasks": navigation_tasks # ПРОВЕРЬ ЭТО ИМЯ!
    })