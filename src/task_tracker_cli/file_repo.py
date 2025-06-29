import repo_utils as ru
from .models import Task

class JsonFileRepo:

    def __init__(self):
        self._tasks: list[Task] = ru.load_tasks()

    def create_task(self, description: str):
        self._tasks.append(Task(ru.generate_id(), description))
        ru.save_tasks(self._tasks)