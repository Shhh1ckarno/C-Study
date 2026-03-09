from fastapi import APIRouter, Depends, HTTPException

from app.tasks.dao import TasksDAO
from app.tasks.schemas import STaskCreate
from app.users.dependencies import get_current_decoded_token

router = APIRouter(prefix="/tasks", tags=["Задачи"])

@router.post("/create")
async def create_task(data: STaskCreate, decoded_token: dict = Depends(get_current_decoded_token)):
    if decoded_token["role"] != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав для создания задачи")
    await TasksDAO.add_task(data)

@router.delete("/delete/{task_id}")
async def delete_task(task_id: int, decoded_token: dict = Depends(get_current_decoded_token)):
    if decoded_token["role"] != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления задачи")
    await TasksDAO.delete_by_id(task_id)

