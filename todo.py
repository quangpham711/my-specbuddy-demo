"""A small command-line todo application with local JSON persistence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence


DEFAULT_STORAGE_PATH = Path(__file__).with_name("tasks.json")


class TodoStorageError(Exception):
    """Raised when persisted tasks cannot be read safely."""


class TodoTaskNotFoundError(Exception):
    """Raised when a requested task identifier is not stored."""


def load_tasks(storage_path: Path) -> list[dict[str, object]]:
    """Load and validate the ordered task list at *storage_path*."""
    if not storage_path.exists():
        return []

    try:
        data = json.loads(storage_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise TodoStorageError(
            f"Could not read task storage '{storage_path}': {error}"
        ) from error

    if not isinstance(data, list):
        raise TodoStorageError("Task storage must contain a JSON array.")

    for task in data:
        if (
            not isinstance(task, dict)
            or not isinstance(task.get("id"), int)
            or not isinstance(task.get("description"), str)
        ):
            raise TodoStorageError("Task storage contains an invalid task entry.")
        if "completed" not in task:
            task["completed"] = False
        elif not isinstance(task["completed"], bool):
            raise TodoStorageError("Task storage contains an invalid completion state.")

    return data


def save_tasks(storage_path: Path, tasks: list[dict[str, object]]) -> None:
    """Write tasks as readable JSON, creating the storage directory if needed."""
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    storage_path.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")


def add_task(description: str, storage_path: Path) -> dict[str, object]:
    """Add a task and return its persisted representation."""
    tasks = load_tasks(storage_path)
    next_id = max((int(task["id"]) for task in tasks), default=0) + 1
    task: dict[str, object] = {
        "id": next_id,
        "description": description,
        "completed": False,
    }
    tasks.append(task)
    save_tasks(storage_path, tasks)
    return task


def complete_task(task_id: int, storage_path: Path) -> dict[str, object]:
    """Mark the task identified by *task_id* as completed and persist it."""
    tasks = load_tasks(storage_path)
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(storage_path, tasks)
            return task
    raise TodoTaskNotFoundError(f"No task found with ID {task_id}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a local todo list.")
    commands = parser.add_subparsers(dest="command", required=True)

    add_parser = commands.add_parser("add", help="Add a task")
    add_parser.add_argument("description", nargs="*", help="Task description")
    commands.add_parser("list", help="List saved tasks")
    complete_parser = commands.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", type=int, help="Task ID")
    return parser


def main(argv: Sequence[str] | None = None, storage_path: Path | None = None) -> int:
    """Run the todo CLI and return a process exit code."""
    args = build_parser().parse_args(argv)
    path = storage_path or DEFAULT_STORAGE_PATH

    try:
        if args.command == "add":
            description = " ".join(args.description).strip()
            if not description:
                print("Error: task description must not be empty.", file=sys.stderr)
                return 2

            task = add_task(description, path)
            print(f"Added task {task['id']}: {task['description']}")
            return 0

        if args.command == "complete":
            task = complete_task(args.task_id, path)
            print(f"Completed task {task['id']}: {task['description']}")
            return 0

        tasks = load_tasks(path)
        if not tasks:
            print("No tasks found.")
            return 0

        for task in tasks:
            status = "[x]" if task["completed"] else "[ ]"
            print(f"{status} {task['id']}. {task['description']}")
        return 0
    except TodoStorageError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except TodoTaskNotFoundError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Error: could not save task storage '{path}': {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
