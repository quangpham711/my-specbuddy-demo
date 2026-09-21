# Design

## Context

The existing `todo.py` stores an ordered JSON array of task objects with `id` and `description`, and its `list` command prints every task. See `proposal.md` for motivation and `specs/todo-management/spec.md` for the behavioral changes. Existing user-created JSON files must remain usable.

## Goals / Non-Goals

**Goals:**

- Add a simple completion action identified by the task IDs already shown to users.
- Preserve compatibility with task entries written before completion tracking existed.
- Make status scannable in list output without changing creation order.

**Non-Goals:**

- Reopening completed tasks, deleting tasks, filtering lists, or changing task identifiers.
- Rewriting an existing storage file solely to add default fields.

## Decisions

- Add `complete <task-id>` as an `argparse` subcommand. Task IDs already form the public reference in list output, so a separate identifier is unnecessary.
- Extend newly created task objects with a boolean `completed: false`. When loading legacy task objects that omit the field, interpret the state as incomplete. This preserves pre-existing JSON data without a migration command.
- Change `list` output to prefix each task with `[ ]` for incomplete or `[x]` for completed, followed by its existing ID and description. The markers are concise and make status visible while retaining order and IDs.
- Marking an already completed task is idempotent: preserve its completed state and return a success confirmation. This avoids making repeated user commands an error.

## Risks / Trade-offs

- [Older JSON entries lack the new field] → Default a missing field to incomplete during load and persist the field when the task list is next saved.
- [A non-numeric or unknown task ID is supplied] → Use command parsing and explicit lookup errors; do not write the storage file on lookup failure.
- [Changed list formatting affects users copying output] → Keep task IDs and descriptions visible in the same creation order, adding only a status prefix.

## Migration Plan

No explicit migration is required. Existing task files load with missing completion fields treated as incomplete; the app adds the field only when a subsequent save occurs. Rolling back the code leaves the extra JSON field unused by the prior implementation.
