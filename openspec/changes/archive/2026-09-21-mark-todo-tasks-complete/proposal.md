# Proposal

## Why

Users can add and view tasks but cannot record when work is finished. Adding completion tracking lets the todo list represent both outstanding and completed work without removing task history.

## What Changes

- Add a `complete <task-id>` command that marks an existing task as completed.
- Persist each task's completion state in the existing local JSON store.
- Display each task's completion state in `list` output.
- Report a clear error when a supplied task identifier does not match a saved task.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `todo-management`: Support persisted task completion state, completion by task identifier, and completion-aware task listing.

## Impact

- Updates `todo.py`, its standard-library tests, and README command documentation.
- Extends existing JSON task entries compatibly by treating records without completion state as incomplete.
- Adds no external dependencies or APIs.
