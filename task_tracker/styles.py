from questionary import Style
from task_storage import Status

# Status values
STATUS_TODO = Status.TODO.value
STATUS_IN_PROGRESS = Status.IN_PROGRESS.value
STATUS_DONE = Status.DONE.value

# Generic status to color mapping
STATUS_COLOR = {
    STATUS_TODO: "yellow",
    STATUS_IN_PROGRESS: "cyan",
    STATUS_DONE: "green",
}


# Helper: status to questionary style class name
def status_to_class(status):
    return f"class:{status.replace('-', '_')}"


# Helper: status to questionary fg color (for Style)
def status_to_fg(status):
    color = STATUS_COLOR.get(status, "white")
    return f"fg:{color}"


# Build questionary Style dynamically from STATUS_COLOR
choice_style = Style(
    [(status.replace("-", "_"), status_to_fg(status)) for status in STATUS_COLOR]
)

# Map status to style class for questionary Choice labels
STATUS_CLASS = {status: status_to_class(status) for status in STATUS_COLOR}
