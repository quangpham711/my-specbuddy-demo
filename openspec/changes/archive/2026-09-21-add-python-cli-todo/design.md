# Design

## Context

The repository currently contains only documentation and OpenSpec artifacts. See `proposal.md` for motivation and `specs/todo-management/spec.md` for required behavior. The app must be runnable with a standard Python installation and retain data across independent invocations.

## Goals / Non-Goals

**Goals:**

- Offer a discoverable `add` and `list` command interface.
- Keep task storage human-readable and local to the project.
- Keep the implementation dependency-free and small enough for a demo project.

**Non-Goals:**

- Task completion state, editing, deletion, due dates, or multi-user synchronization.
- A database, web interface, package publishing, or cloud backup.

## Decisions

- Use a root-level `todo.py` entry point with Python's standard `argparse` module. Users will run `python3 todo.py add "description"` and `python3 todo.py list`; this is explicit and needs no packaging setup. A console-script package was considered but would add configuration outside this small app's scope.
- Store tasks in a root-level `tasks.json` file as an ordered JSON array of task objects containing an integer identifier and description. JSON is portable, inspectable, and supported by Python's standard library; a database would be unnecessary complexity.
- Read storage for each command invocation and write it after successful additions. The missing-file case represents an empty task list. This directly supports persistence without requiring a background process.
- Use `unittest` tests that invoke the CLI logic against a temporary storage location. This validates command behavior and persistence without leaving test data in the repository. A third-party test framework was considered but would violate the dependency-free goal.

## Risks / Trade-offs

- [A user edits or corrupts the JSON file] → Report a clear error rather than silently discarding data.
- [Concurrent commands can overwrite each other's writes] → Accept this limitation for the single-user local demo; concurrent access is out of scope.
- [Runtime data appears as an untracked repository file] → Document the file's purpose and exclude it from version control if a `.gitignore` is introduced.

## Migration Plan

No migration is required because this introduces a new application and creates storage only when a user adds the first task.
