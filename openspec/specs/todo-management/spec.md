# todo-management Specification

## Purpose

Provide a small command-line interface for creating and viewing todo tasks that remain available after the command exits.

## Requirements

### Requirement: Add todo tasks
The system SHALL provide an `add` command that accepts a non-empty task description, saves the task, and confirms the addition in terminal output. The system SHALL reject an empty task description without saving a task.

#### Scenario: Add a task
- **WHEN** a user runs the `add` command with a non-empty description
- **THEN** the system saves the task and displays a confirmation

#### Scenario: Reject an empty task
- **WHEN** a user runs the `add` command without a non-empty description
- **THEN** the system displays an error and does not save a task

### Requirement: Persist tasks locally
The system SHALL store added tasks in a local JSON file, including each task's completion state, and SHALL load previously stored tasks when a later command invocation runs. The system SHALL treat a previously stored task without a completion state as incomplete.

#### Scenario: Task survives a new invocation
- **WHEN** a user adds a task and subsequently runs the CLI again from the same project directory
- **THEN** the previously added task is available to the later invocation

#### Scenario: Existing task data has no completion state
- **WHEN** the CLI loads a saved task that has no completion state field
- **THEN** the system treats the task as incomplete

### Requirement: List todo tasks
The system SHALL provide a `list` command that displays every saved task in creation order with a visible completed or incomplete status. When no tasks are saved, the system SHALL display a clear empty-list message.

#### Scenario: List saved tasks
- **WHEN** a user runs the `list` command after adding one or more tasks
- **THEN** the system displays all saved task descriptions and their completion statuses in creation order

#### Scenario: List with no saved tasks
- **WHEN** a user runs the `list` command before any task has been saved
- **THEN** the system displays a clear message that no tasks exist

### Requirement: Complete todo tasks
The system SHALL provide a `complete` command that accepts a saved task identifier and marks that task as completed. The system SHALL persist the completed state and confirm the update in terminal output. When the identifier does not match a saved task, the system SHALL display an error and leave saved tasks unchanged.

#### Scenario: Complete an existing task
- **WHEN** a user runs the `complete` command with the identifier of an incomplete saved task
- **THEN** the system persists that task as completed and displays a confirmation

#### Scenario: Complete an unknown task
- **WHEN** a user runs the `complete` command with an identifier that does not match a saved task
- **THEN** the system displays an error and does not modify saved tasks
