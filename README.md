# My SpecBuddy Demo

This repository is a small demo project for working with OpenSpec, a structured workflow for planning and tracking changes.

## Todo CLI

The project includes a small todo app that uses only Python's standard library. Run it with Python 3:

```bash
python3 todo.py add "Buy milk"
python3 todo.py complete 1
python3 todo.py list
```

Tasks are saved in `tasks.json` beside `todo.py`, so they remain available between commands. The file is created when you add your first task and is excluded from version control.

The `complete` command marks a task by its ID. The list uses `[ ]` for incomplete tasks and `[x]` for completed tasks.
