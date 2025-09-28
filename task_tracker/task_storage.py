# Task storage and model for TaskTrackerCLI
import json
import os
from typing import List, Optional
from enum import Enum
from datetime import datetime, timezone


class Status(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Task:
    def __init__(
        self,
        id: int,
        description: str,
        status: Status = Status.TODO,
        createdAt: Optional[str] = None,
        updatedAt: Optional[str] = None,
    ):
        self.id = id
        self.description = description
        self.status = status

        now = datetime.now(timezone.utc).isoformat()
        self.createdAt = createdAt or now
        self.updatedAt = updatedAt or now

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            description=data["description"],
            status=Status(data["status"]),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt"),
        )


class TaskStorage:
    FILENAME = ".tasktracker_tasks.json"

    def __init__(self, directory: Optional[str] = None):
        self.directory = directory or os.getcwd()
        self.filepath = os.path.join(self.directory, self.FILENAME)
        self.tasks = self._load()

    def _load(self) -> List[Task]:
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r") as f:
            data = json.load(f)
            return [Task.from_dict(t) for t in data]

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def add(self, description: str, status: Status = Status.TODO) -> Task:
        new_id = 1 if not self.tasks else max(t.id for t in self.tasks) + 1
        task = Task(new_id, description, status=status)
        self.tasks.append(task)
        self._save()
        return task

    def update(self, id: int, description: str) -> bool:
        for t in self.tasks:
            if t.id == id:
                t.description = description
                t.updatedAt = datetime.now(timezone.utc).isoformat()
                self._save()
                return True
        return False

    def delete(self, id: int) -> bool:
        for i, t in enumerate(self.tasks):
            if t.id == id:
                del self.tasks[i]
                self._save()
                return True
        return False

    def set_status(self, id: int, status: Status) -> bool:
        for t in self.tasks:
            if t.id == id:
                t.status = status
                t.updatedAt = datetime.now(timezone.utc).isoformat()
                self._save()
                return True
        return False

    def list(self, status: Optional[Status] = None) -> List[Task]:
        if status:
            return [t for t in self.tasks if t.status == status]
        return self.tasks
