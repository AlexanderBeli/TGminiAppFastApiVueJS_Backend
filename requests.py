from typing import List

from pydantic import BaseModel, ConfigDict
from sqlalchemy import delete, func, select, update

from models import Task, User, async_session


class TaskSchema(BaseModel):
    id: int
    title: str
    completed: bool
    user: int

    # чтобы сериализация работала корректно
    model_config = ConfigDict(from_attributes=True)


async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user

        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)  # для того, чтобы его вернуть
        return new_user


async def get_tasks(user_id):
    async with async_session() as session:
        # scalars так как много задач
        tasks = await session.scalars(
            select(Task).where(Task.user == user_id, Task.completed == False)
        )

        serialized_tasks = [TaskSchema.model_validate(t).model_dump for t in tasks]

        return serialized_tasks


async def get_completed_tasks_count(user_id):
    async with async_session() as session:
        return await session.scalar(
            select(func.count(Task.id)).where(Task.completed == True)
        )


async def add_task(user_id, title):
    async with async_session() as session:
        new_task = Task(title=title, user=user_id)
        session.add(new_task)
        await session.commit()


async def update_task(task_id):
    async with async_session() as session:
        await session.execute(
            update(Task).where(Task.id == task_id).value(completed=True)
        )
        await session.commit()
