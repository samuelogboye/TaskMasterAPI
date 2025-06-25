from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import TaskCreate, Task
from app.repositories.tasks import TaskRepository
from app.database import get_db
from app.exceptions import TaskNotFoundError

router = APIRouter()

@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_description="The created task"
)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new task with the following details:
    - **title**: required, must be 1-100 characters
    - **description**: optional, max 500 characters
    """
    repo = TaskRepository(db)
    return repo.create_task(task)

@router.get(
    "/",
    response_model=list[Task],
    summary="Get all tasks",
    response_description="List of all tasks"
)
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve all tasks in the system"""
    repo = TaskRepository(db)
    return repo.get_tasks(skip, limit)

@router.get(
    "/{task_id}",
    response_model=Task,
    summary="Get a specific task",
    responses={
        404: {"description": "Task not found"}
    }
)
async def get_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific task by its ID
    
    - **task_id**: UUID of the task to retrieve
    """
    repo = TaskRepository(db)
    task = repo.get_task(task_id)
    if not task:
        raise TaskNotFoundError(task_id=task_id)
    return task