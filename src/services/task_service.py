from math import ceil
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate, TaskListResponse, TaskResponse


async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    db_task = Task(**task_data.model_dump(), user_id=user_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_tasks(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 10
) -> TaskListResponse:
    count_query = select(func.count()).select_from(Task).where(Task.user_id == user_id)
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(query)
    tasks = result.scalars().all()

    page = skip // limit + 1
    total_pages = ceil(total / limit) if total > 0 else 1

    return TaskListResponse(
        tasks=[TaskResponse.model_validate(task) for task in tasks],
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages
    )


async def get_task_by_id(db: AsyncSession, task_id: int, user_id: int) -> Task:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


async def update_task(
    db: AsyncSession,
    task_id: int,
    task_data: TaskUpdate,
    user_id: int
) -> Task:
    task = await get_task_by_id(db, task_id, user_id)

    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> None:
    task = await get_task_by_id(db, task_id, user_id)
    await db.execute(delete(Task).where(Task.id == task_id))
    await db.commit()
