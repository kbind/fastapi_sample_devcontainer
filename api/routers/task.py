from fastapi import APIRouter

import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks", response_model=list[task_schema.Task])
async def list_tasks():
    return [task_schema.Task(id=1, title="1つめのToDoタスク")]

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate):
    # return task_schema.TaskCreateResponse(id=1, title=task_body.title, done=task_body.done)と等価
    return task_schema.TaskCreateResponse(id=1, **task_body.dict())

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())

@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int):
    return