# TaskTrackerCLI

A simple, interactive command-line task tracker built with Typer, Rich, and Questionary.

## Features
- Add, update, delete tasks from the command line
- Mark tasks as in-progress or done
- List tasks with color-coded status (TODO, IN-PROGRESS, DONE)
- Interactive selection for update/delete/mark commands
- Persistent storage in a local JSON file

## Installation

### Local (user or system-wide)
From the project root directory:

```sh
uv pip install .
```
Or with pip:
```sh
pip install .
```

### In a virtual environment
```sh
python -m venv venv
source venv/bin/activate
uv pip install .
# or
pip install .
```

## Usage
After installation, use the CLI command:

```sh
tasktracker list
```

Other commands:
- `tasktracker add "Task description"`
- `tasktracker update`
- `tasktracker delete`
- `tasktracker mark-in-progress`
- `tasktracker mark-done`

For help:
```sh
tasktracker --help
```

## Development & Testing

Run tests:
```sh
pytest
```

## Inspiration

[Roadmap Backend Projects](https://roadmap.sh/projects/task-tracker) 