from datetime import datetime
from . import repo_utils as ru
from .models import Task, Status

class JsonFileRepo:

    def __init__(self):
        self._tasks: dict[int, Task] = ru.load_tasks()

    def _save_changes(self):
        ru.save_tasks(self._tasks.values())

    def create(self, description: str) -> Task:
        new_task = Task(ru.generate_id(), description)
        self._tasks[new_task.id] = new_task
        self._save_changes()
        return new_task

    def get_by_id(self, id: int) -> Task:
        return self._tasks[id]
    
    def get_by_status(self, status: Status) -> list[Task]:
        return filter(lambda t: t.status == status, self._tasks.values())
    
    def set_status(self, id: int, status: Status) -> Task:
        task = self._tasks[id]
        task.status = status
        task.updatedAt = datetime.now()
        self._save_changes()
        return task

    def set_description(self, id: int, description: str) -> Task:
        task = self._tasks[id]
        task.description = description
        task.updatedAt = datetime.now()
        self._save_changes()
        return task
    
    def delete(self, id: int):
        self._tasks.pop(id)
        self._save_changes()

    @property
    def tasks(self) -> dict[int, Task]:
        return self._tasks