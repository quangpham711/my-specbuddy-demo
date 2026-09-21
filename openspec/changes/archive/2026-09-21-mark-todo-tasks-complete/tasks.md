# Tasks

## 1. Completion Behavior

- [x] 1.1 Extend the task storage model and `add` command to persist `completed: false` for new tasks while accepting legacy task entries without that field; verify a legacy JSON task lists as incomplete.
- [x] 1.2 Add `complete <task-id>` to the CLI, persist a matching task as completed, and leave storage unchanged for an unknown ID; verify both commands and their terminal output.
- [x] 1.3 Update `list` output to show `[ ]` or `[x]` status markers in creation order; verify an incomplete and completed task are both displayed correctly.

## 2. Verification and Documentation

- [x] 2.1 Extend `unittest` coverage for completion persistence, unknown IDs, legacy JSON compatibility, and completion-aware listing; verify with `python3 -m unittest`.
- [x] 2.2 Document `python3 todo.py complete <task-id>` and list status markers in README.md; verify the examples match `python3 todo.py --help` and CLI output.
