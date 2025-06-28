from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any

class Status(Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3

@dataclass
class Task:
    _id: int
    description: str
    createdAt: datetime = field(default=datetime.now())
    updatedAt: datetime = field(default=datetime.now())
    status: Status = field(default=Status.TODO)

    @property
    def id(self) -> int:
        return self._id

    def todict(self) -> dict[str, Any]:
        return {
            'id': self._id,
            'description': self.description,
            'createdAt': self.createdAt.isoformat(),
            'updatedAt': self.updatedAt.isoformat(),
            'status': self.status.value
            }

    @classmethod
    def fromdict(cls, dict: dict[str, Any]) -> 'Task':
        return Task(
            _id=dict['id'], 
            description=dict['description'], 
            createdAt=datetime.fromisoformat(dict['createdAt']), 
            updatedAt=datetime.fromisoformat(dict['updatedAt']), 
            status=Status(dict['status']))