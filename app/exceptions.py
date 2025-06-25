from fastapi import HTTPException, status


class TaskNotFoundError(HTTPException):
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
