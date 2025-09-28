import typer
from rich.console import Console
from rich.panel import Panel
from commands import app as commands_app
import sys

app = typer.Typer()
app.add_typer(commands_app)
console = Console()


@app.callback()
def main():
    """Task Tracker CLI App"""
    # Gather commands and help from commands_app (Typer)
    commands_info = []
    for cmd_info in commands_app.registered_commands:
        name = cmd_info.name
        help_text = cmd_info.help or ""
        commands_info.append(f"[bold yellow]{name}[/bold yellow]: {help_text}")
    commands_str = "\n".join(commands_info)
    console.print(
        Panel.fit(
            "[bold green]Welcome to TaskTrackerCLI![/bold green]\n\n"
            "A simple CLI app to track your tasks (CRUD).\n\n"
            "[bold]Available commands:[/bold]\n"
            f"{commands_str}\n\n"
            "Use [bold yellow]--help[/bold yellow] for more details.",
            title="[cyan]Task Tracker CLI",
            border_style="bright_blue",
        )
    )


if __name__ == "__main__":
    # If no arguments are provided, show help
    if len(sys.argv) == 1:
        sys.argv.append("--help")
    app()
