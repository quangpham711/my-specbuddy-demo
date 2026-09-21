# Tasks

## 1. CLI and Storage

- [x] 1.1 Implement `todo.py` with `add` and `list` commands backed by a root-level JSON task store, and verify `python3 todo.py add "Buy milk"` succeeds and creates valid JSON.
- [x] 1.2 Handle missing storage as an empty list, reject empty add descriptions, and report unreadable JSON without destroying it; verify each case returns clear terminal output.

## 2. Verification and Documentation

- [x] 2.1 Add standard-library `unittest` coverage for adding, listing, empty-list behavior, validation, and persistence across separate CLI executions; verify with `python3 -m unittest`.
- [x] 2.2 Document the add/list commands and local `tasks.json` storage in README.md, exclude runtime task data from version control, and verify the documented commands match the CLI interface.
