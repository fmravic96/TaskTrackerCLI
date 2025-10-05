import tempfile
import pytest
from typer.testing import CliRunner
from task_tracker import commands
from task_tracker.task_storage import Status, TaskStorage

runner = CliRunner()


@pytest.fixture(autouse=True)
def temp_tasktracker_dir(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.chdir(tmpdir)
        yield tmpdir


def get_storage():
    return TaskStorage()


def test_add_task():
    result = runner.invoke(commands.app, ["add", "Test task"])
    assert result.exit_code == 0
    storage = get_storage()
    tasks = storage.list()
    assert len(tasks) == 1
    assert tasks[0].description == "Test task"
    assert tasks[0].status == Status.TODO


def test_update_task():
    runner.invoke(commands.app, ["add", "Initial"])
    storage = get_storage()
    task_id = storage.list()[0].id
    result = runner.invoke(commands.app, ["update", str(task_id), "Updated desc"])
    assert result.exit_code == 0
    t = get_storage().list()[0]
    assert t.description == "Updated desc"
    assert t.updatedAt >= t.createdAt


def test_delete_task():
    runner.invoke(commands.app, ["add", "To delete"])
    storage = get_storage()
    task_id = storage.list()[0].id
    result = runner.invoke(commands.app, ["delete", str(task_id)])
    assert result.exit_code == 0
    assert len(get_storage().list()) == 0


def test_set_status():
    runner.invoke(commands.app, ["add", "Status test"])
    storage = get_storage()
    task_id = storage.list()[0].id
    result = runner.invoke(commands.app, ["mark-in-progress", str(task_id)])
    assert result.exit_code == 0
    t = get_storage().list()[0]
    assert t.status == Status.IN_PROGRESS
    result = runner.invoke(commands.app, ["mark-done", str(task_id)])
    assert result.exit_code == 0
    t = get_storage().list()[0]
    assert t.status == Status.DONE


def test_list_by_status():
    from tests.factory import TaskFactory

    # Create two tasks, one TODO and one DONE
    a = TaskFactory(description="A", status=Status.TODO)
    b = TaskFactory(description="B", status=Status.DONE)
    storage = get_storage()
    storage.tasks = [a, b]
    storage._save()

    # Use CLI to list TODO tasks
    result_todo = runner.invoke(commands.app, ["list", "todo"])
    assert result_todo.exit_code == 0
    assert "A" in result_todo.output
    assert "B" not in result_todo.output

    # Use CLI to list DONE tasks
    result_done = runner.invoke(commands.app, ["list", "done"])
    assert result_done.exit_code == 0
    assert "B" in result_done.output
    assert "A" not in result_done.output
