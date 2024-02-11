from sqlalchemy.orm import Session
import api.models.task as task_model
import api.schemas.task as task_schema

def create_task(db: Session, task_create: task_schema.TaskCreate) -> task_model.Task:
    # DBモデルに変換
    task = task_model.Task(**task_create.dict())
    db.add(task)
    db.commit()
    # 記録されたDB上のデータを元にtaskを更新
    db.refresh(task)
    return task
