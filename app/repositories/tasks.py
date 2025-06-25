from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_tasks(self, user_id: str, skip: int = 0, limit: int = 100):
        return (
            self.db.query(Task)
            .filter(Task.owner_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_task(self, task_id: str):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create_user_task(self, user_id: str, task: TaskCreate):
        db_task = Task(**task.model_dump(), owner_id=user_id)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def update_user_task(self, user_task: Task, task: TaskCreate):
        # db_task = self.get_user_task(user_id, task_id)
        # if not db_task:
        #     return None

        for key, value in task.model_dump().items():
            setattr(user_task, key, value)

        self.db.commit()
        self.db.refresh(user_task)
        return user_task

    def delete_task(self, user_task: Task):
        self.db.delete(user_task)
        self.db.commit()
        return True
