import os
from tests.factory import TaskFactory
from task_tracker.task_storage import Status, TaskStorage


def generate_dummy_tasks():
    # Clean up storage file before generating tasks
    storage_file = os.path.join(os.getcwd(), TaskStorage.FILENAME)
    if os.path.exists(storage_file):
        os.remove(storage_file)
    storage = TaskStorage()
    tasks = []
    for status in [Status.TODO, Status.IN_PROGRESS, Status.DONE]:
        for _ in range(5):
            task = TaskFactory(status=status)
            saved_task = storage.add(task.description, status=status)
            tasks.append(saved_task)
    return tasks


if __name__ == "__main__":
    tasks = generate_dummy_tasks()
    for task in tasks:
        print(
            f"Task(id={task.id}, description='{task.description}', status={task.status}, createdAt={task.createdAt}, updatedAt={task.updatedAt})"
        )
