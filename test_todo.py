"""Tests for the local todo command-line application."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TodoCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.project_path = Path(self.temporary_directory.name)
        self.storage_path = self.project_path / "tasks.json"
        self.script_path = self.project_path / "todo.py"
        shutil.copy(Path(__file__).with_name("todo.py"), self.script_path)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_cli(self, *arguments: str) -> tuple[int, str, str]:
        result = subprocess.run(
            [sys.executable, str(self.script_path), *arguments],
            cwd=self.project_path,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout, result.stderr

    def test_list_reports_empty_storage(self) -> None:
        exit_code, stdout, stderr = self.run_cli("list")

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout, "No tasks found.\n")
        self.assertEqual(stderr, "")

    def test_add_and_list_persist_tasks_in_creation_order(self) -> None:
        first_exit_code, first_stdout, _ = self.run_cli("add", "Buy milk")
        second_exit_code, second_stdout, _ = self.run_cli("add", "Write tests")
        list_exit_code, list_stdout, list_stderr = self.run_cli("list")

        self.assertEqual(first_exit_code, 0)
        self.assertEqual(first_stdout, "Added task 1: Buy milk\n")
        self.assertEqual(second_exit_code, 0)
        self.assertEqual(second_stdout, "Added task 2: Write tests\n")
        self.assertEqual(list_exit_code, 0)
        self.assertEqual(list_stdout, "[ ] 1. Buy milk\n[ ] 2. Write tests\n")
        self.assertEqual(list_stderr, "")

        stored_tasks = json.loads(self.storage_path.read_text(encoding="utf-8"))
        self.assertEqual(
            stored_tasks,
            [
                {"id": 1, "description": "Buy milk", "completed": False},
                {"id": 2, "description": "Write tests", "completed": False},
            ],
        )

    def test_complete_persists_status_and_list_displays_completed_task(self) -> None:
        self.run_cli("add", "Buy milk")

        exit_code, stdout, stderr = self.run_cli("complete", "1")

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout, "Completed task 1: Buy milk\n")
        self.assertEqual(stderr, "")
        self.assertEqual(
            json.loads(self.storage_path.read_text(encoding="utf-8")),
            [{"id": 1, "description": "Buy milk", "completed": True}],
        )

        list_exit_code, list_stdout, list_stderr = self.run_cli("list")

        self.assertEqual(list_exit_code, 0)
        self.assertEqual(list_stdout, "[x] 1. Buy milk\n")
        self.assertEqual(list_stderr, "")

    def test_complete_unknown_task_does_not_change_storage(self) -> None:
        self.run_cli("add", "Buy milk")
        original_storage = self.storage_path.read_text(encoding="utf-8")

        exit_code, stdout, stderr = self.run_cli("complete", "99")

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "Error: No task found with ID 99.\n")
        self.assertEqual(self.storage_path.read_text(encoding="utf-8"), original_storage)

    def test_legacy_task_without_completion_state_is_incomplete(self) -> None:
        self.storage_path.write_text(
            '[{"id": 7, "description": "Legacy task"}]\n',
            encoding="utf-8",
        )

        exit_code, stdout, stderr = self.run_cli("list")

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout, "[ ] 7. Legacy task\n")
        self.assertEqual(stderr, "")

    def test_add_rejects_an_empty_description_without_creating_storage(self) -> None:
        exit_code, stdout, stderr = self.run_cli("add", "   ")

        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("task description must not be empty", stderr)
        self.assertFalse(self.storage_path.exists())

    def test_invalid_json_is_reported_without_overwriting_storage(self) -> None:
        invalid_json = "{not valid json\n"
        self.storage_path.write_text(invalid_json, encoding="utf-8")

        exit_code, stdout, stderr = self.run_cli("list")

        self.assertEqual(exit_code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("Could not read task storage", stderr)
        self.assertEqual(self.storage_path.read_text(encoding="utf-8"), invalid_json)


if __name__ == "__main__":
    unittest.main()
