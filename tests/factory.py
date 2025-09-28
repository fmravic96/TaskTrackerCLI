from factory.base import Factory
from factory.declarations import Sequence, LazyAttribute
from faker import Faker as PyFaker
from task_tracker.task_storage import Task


class TaskFactory(Factory):
    class Meta:
        model = Task

    id = Sequence(lambda n: n + 1)
    description = LazyAttribute(lambda o: f"Dummy task {o.id}")
    createdAt = LazyAttribute(lambda o: PyFaker().date_time_this_year().isoformat())
    updatedAt = LazyAttribute(lambda o: PyFaker().date_time_this_year().isoformat())
