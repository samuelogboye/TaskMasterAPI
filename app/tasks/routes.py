from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.service import get_current_user
from app.auth.models import User
from .schemas import TaskCreate, Task
from .repository import TaskRepository


router = APIRouter(tags=["tasks"])


@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_description="The created task",
)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new task with the following details:
    - **title**: required, must be 1-100 characters
    - **description**: optional, max 500 characters
    """
    try:
        repo = TaskRepository(db)
        return repo.create_user_task(current_user.id, task)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Task creation failed",
                "code": "TASK_CREATION_ERROR",
                "message": "Could not complete task creation",
            },
        ) from e


@router.get(
    "/",
    response_model=list[Task],
    summary="Get all tasks",
    response_description="List of all tasks",
)
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all tasks for the current user"""
    try:
        repo = TaskRepository(db)
        return repo.get_user_tasks(current_user.id, skip, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Task retrieval failed",
                "code": "TASK_RETRIEVAL_ERROR",
                "message": "Could not complete task retrieval",
            },
        ) from e


@router.get(
    "/{task_id}",
    response_model=Task,
    summary="Get a specific task",
    responses={404: {"description": "Task not found"}},
)
async def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a specific task by its ID

    - **task_id**: UUID of the task to retrieve
    """
    try:
        repo = TaskRepository(db)

        task = repo.get_task(task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        if current_user.id != task.owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this task",
            )

        return task
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Task retrieval failed",
                "code": "TASK_RETRIEVAL_ERROR",
                "message": "Could not complete task retrieval",
            },
        ) from e


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a task

    - **task_id**: UUID of the task to update
    - **title**: updated title
    - **description**: updated description
    """
    try:
        repo = TaskRepository(db)

        user_task = repo.get_task(task_id)

        if not user_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        if current_user.id != user_task.owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this task",
            )

        updated_task = repo.update_user_task(user_task, task)

        return updated_task
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Task update failed",
                "code": "TASK_UPDATE_ERROR",
                "message": "Could not complete task update",
            },
        ) from e


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a task

    - **task_id**: UUID of the task to delete
    """
    try:
        repo = TaskRepository(db)

        user_task = repo.get_task(task_id)

        if not user_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        if current_user.id != user_task.owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this task",
            )

        repo.delete_task(user_task)

        return None
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Task deletion failed",
                "code": "TASK_DELETION_ERROR",
                "message": "Could not complete task deletion",
            },
        ) from e
