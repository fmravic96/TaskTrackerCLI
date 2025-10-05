import typer
import questionary
from rich.console import Console
from questionary import Choice
from rich.console import Console
from rich.table import Table

from task_tracker.styles import STATUS_CLASS, choice_style, STATUS_COLOR
from task_tracker.task_storage import TaskStorage, Status

console = Console()
app = typer.Typer()


@app.command()
def add(description: str = typer.Argument(None, show_default=False)):
    """Add a new task. If no description is given, prompt the user."""
    if description is None:
        description = typer.prompt("Enter task name")
    storage = TaskStorage()
    task = storage.add(description)
    console.print(f"[green]Task added successfully (ID: {task.id})[/green]")


@app.command()
def update(
    id: int = typer.Argument(None, show_default=False),
    description: str = typer.Argument(None, show_default=False),
):
    """Update a task's description. If no ID is given, prompt to select a task."""
    storage = TaskStorage()
    if id is None:
        tasks = storage.list()
        if not tasks:
            console.print("[yellow]No tasks available to update.[/yellow]")
            raise typer.Exit(1)
        choices = []
        for t in tasks:
            status = t.status.value
            status_class = STATUS_CLASS.get(status, "class:text")
            label = [
                ("class:text", f"{t.description} ["),
                (status_class, t.status.value.upper()),
                ("class:text", "]"),
            ]
            choices.append(Choice(title=label, value=t.id))
        id = questionary.select(
            "Select a task to update:", choices=choices, style=choice_style
        ).ask()
        if id is None:
            raise typer.Exit(1)
    if description is None:
        description = typer.prompt("Enter new description")
    if storage.update(id, description):
        console.print(f"[yellow]Task {id} updated.[/yellow]")
    else:
        console.print(f"[red]Task {id} not found.[/red]")


@app.command()
def delete(id: int = typer.Argument(None, show_default=False)):
    """Delete a task by ID. If no ID is given, prompt to select a task."""
    storage = TaskStorage()
    if id is None:
        tasks = storage.list()
        if not tasks:
            console.print("[yellow]No tasks available to delete.[/yellow]")
            raise typer.Exit(1)
        choices = []
        for t in tasks:
            status = t.status.value
            status_class = STATUS_CLASS.get(status, "class:text")
            label = [
                ("class:text", f"{t.description} ["),
                (status_class, t.status.value.upper()),
                ("class:text", "]"),
            ]
            choices.append(Choice(title=label, value=t.id))
        id = questionary.select(
            "Select a task to delete:", choices=choices, style=choice_style
        ).ask()
        if id is None:
            raise typer.Exit(1)
    if storage.delete(id):
        console.print(f"[red]Task {id} deleted.[/red]")
    else:
        console.print(f"[red]Task {id} not found.[/red]")


@app.command("mark-in-progress")
def mark_in_progress(id: int = typer.Argument(None, show_default=False)):
    """Mark a task as in progress. If no ID is given, prompt to select a task."""
    storage = TaskStorage()
    if id is None:
        tasks = storage.list()
        if not tasks:
            console.print("[yellow]No tasks available to mark as in progress.[/yellow]")
            raise typer.Exit(1)
        choices = []
        for t in tasks:
            status = t.status.value
            status_class = STATUS_CLASS.get(status, "class:text")
            label = [
                ("class:text", f"{t.description} ["),
                (status_class, t.status.value.upper()),
                ("class:text", "]"),
            ]
            choices.append(Choice(title=label, value=t.id))
        id = questionary.select(
            "Select a task to mark as in progress:", choices=choices, style=choice_style
        ).ask()
        if id is None:
            raise typer.Exit(1)
    if storage.set_status(id, Status.IN_PROGRESS):
        console.print(f"[cyan]Task {id} marked as in progress.[/cyan]")
    else:
        console.print(f"[red]Task {id} not found.[/red]")


@app.command("mark-done")
def mark_done(id: int = typer.Argument(None, show_default=False)):
    """Mark a task as done. If no ID is given, prompt to select a task."""
    storage = TaskStorage()
    if id is None:
        tasks = storage.list()
        if not tasks:
            console.print("[yellow]No tasks available to mark as done.[/yellow]")
            raise typer.Exit(1)
        choices = []
        for t in tasks:
            status = t.status.value
            status_class = STATUS_CLASS.get(status, "class:text")
            label = [
                ("class:text", f"{t.description} ["),
                (status_class, t.status.value.upper()),
                ("class:text", "]"),
            ]
            choices.append(Choice(title=label, value=t.id))
        id = questionary.select(
            "Select a task to mark as done:", choices=choices, style=choice_style
        ).ask()
        if id is None:
            raise typer.Exit(1)
    if storage.set_status(id, Status.DONE):
        console.print(f"[green]Task {id} marked as done.[/green]")
    else:
        console.print(f"[red]Task {id} not found.[/red]")


@app.command()
def list(
    status: str = typer.Argument(None, help="Filter by status: todo, in-progress, done")
):
    """List tasks, optionally filtered by status."""
    storage = TaskStorage()
    status_enum = None
    if status:
        try:
            status_enum = Status(status)
        except ValueError:
            console.print(f"[red]Invalid status: {status}[/red]")
            raise typer.Exit(1)
    tasks = storage.list(status_enum)
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Tasks")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Description", style="white")
    table.add_column("Status")

    for t in tasks:
        color = STATUS_COLOR.get(t.status.value, "white")
        status_text = f"[{color}]{t.status.value.upper()}[/{color}]"
        table.add_row(str(t.id), t.description, status_text)
    console.print(table)
