import tempfile
import pytest
from task_tracker.task_storage import TaskStorage, Status


@pytest.fixture
def temp_storage():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield TaskStorage(directory=tmpdir)


def test_add_task(temp_storage):
    task = temp_storage.add("Test task")
    assert task.id == 1
    assert task.description == "Test task"
    assert task.status == Status.TODO
    assert task.createdAt is not None
    assert task.updatedAt is not None
    assert len(temp_storage.list()) == 1


def test_update_task(temp_storage):
    task = temp_storage.add("Initial")
    updated = temp_storage.update(task.id, "Updated desc")
    assert updated
    t = temp_storage.list()[0]
    assert t.description == "Updated desc"
    assert t.updatedAt >= t.createdAt


def test_delete_task(temp_storage):
    task = temp_storage.add("To delete")
    deleted = temp_storage.delete(task.id)
    assert deleted
    assert len(temp_storage.list()) == 0


def test_set_status(temp_storage):
    task = temp_storage.add("Status test")
    assert temp_storage.set_status(task.id, Status.IN_PROGRESS)
    t = temp_storage.list()[0]
    assert t.status == Status.IN_PROGRESS
    assert temp_storage.set_status(task.id, Status.DONE)
    t = temp_storage.list()[0]
    assert t.status == Status.DONE


def test_list_by_status(temp_storage):
    temp_storage.add("A")
    b = temp_storage.add("B")
    temp_storage.set_status(b.id, Status.DONE)
    todo_tasks = temp_storage.list(Status.TODO)
    done_tasks = temp_storage.list(Status.DONE)
    assert len(todo_tasks) == 1
    assert len(done_tasks) == 1
    assert todo_tasks[0].description == "A"
    assert done_tasks[0].description == "B"
