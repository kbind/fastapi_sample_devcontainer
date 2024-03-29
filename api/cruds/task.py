from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result

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

def get_tasks_with_done(db: Session) -> list[tuple[int, str, bool]]:
    result: Result = db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            # donesテーブルに存在しない場合はNoneを渡す
            task_model.Done.id.isnot(None).label("done"),
        ).outerjoin(task_model.Done)
    )
    # ここでDBレコード取得
    return result.all()

def get_task(db: Session, task_id: int) -> task_model.Task | None:
    # selectの結果が一つでもタプルで返却される
    result: Result = db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    return result.scalars().first()

def update_task(db: Session, task_create: task_schema.TaskCreate, original: task_model.Task) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    db.commit()
    db.refresh(original)
    return original

def delete_task(db: Session, original: task_model.Task) -> None:
    db.delete(original)
    db.commit()
