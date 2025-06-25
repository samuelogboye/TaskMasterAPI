from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate
from datetime import datetime

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tasks(self, skip: int = 0, limit: int = 100):
        return self.db.query(Task).offset(skip).limit(limit).all()

    def get_task(self, task_id: str):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create_task(self, task: TaskCreate):
        db_task = Task(**task.dict())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task