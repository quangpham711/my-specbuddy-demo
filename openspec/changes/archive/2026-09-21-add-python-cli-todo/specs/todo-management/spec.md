# Spec Delta

## Purpose

Provide a small command-line interface for creating and viewing todo tasks that remain available after the command exits.

## ADDED Requirements

### Requirement: Add todo tasks
The system SHALL provide an `add` command that accepts a non-empty task description, saves the task, and confirms the addition in terminal output. The system SHALL reject an empty task description without saving a task.

#### Scenario: Add a task
- **WHEN** a user runs the `add` command with a non-empty description
- **THEN** the system saves the task and displays a confirmation

#### Scenario: Reject an empty task
- **WHEN** a user runs the `add` command without a non-empty description
- **THEN** the system displays an error and does not save a task

### Requirement: Persist tasks locally
The system SHALL store added tasks in a local JSON file and SHALL load previously stored tasks when a later command invocation runs.

#### Scenario: Task survives a new invocation
- **WHEN** a user adds a task and subsequently runs the CLI again from the same project directory
- **THEN** the previously added task is available to the later invocation

### Requirement: List todo tasks
The system SHALL provide a `list` command that displays every saved task in creation order. When no tasks are saved, the system SHALL display a clear empty-list message.

#### Scenario: List saved tasks
- **WHEN** a user runs the `list` command after adding one or more tasks
- **THEN** the system displays all saved task descriptions in their creation order

#### Scenario: List with no saved tasks
- **WHEN** a user runs the `list` command before any task has been saved
- **THEN** the system displays a clear message that no tasks exist
