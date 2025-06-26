import unittest
import os

from main import Task, ToDoListManager

class TestToDoListManager(unittest.TestCase):
    TEST_FILE = "test_tasks.json"

    def setUp(self):
        # Ensure a clean test file for each test
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)
        self.manager = ToDoListManager(filename=self.TEST_FILE)

    def tearDown(self):
        # Clean up test file after each test
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_add_task(self):
        self.manager.add_task("Test Task", "2025-07-01", "high")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].task, "Test Task")
        self.assertEqual(self.manager.tasks[0].due_date, "2025-07-01")
        self.assertEqual(self.manager.tasks[0].priority, "high")
        self.assertFalse(self.manager.tasks[0].done)

    def test_remove_task(self):
        self.manager.add_task("Task to delete", "2025-07-01", "medium")
        self.assertEqual(len(self.manager.tasks), 1)
        self.manager.delete_task(1)
        self.assertEqual(len(self.manager.tasks), 0)

    def test_list_tasks(self):
        self.manager.add_task("Task1", "2025-07-01", "high")
        self.manager.add_task("Task2", "2025-07-02", "low")
        # Capture printed output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        self.manager.list_tasks()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Task1", output)
        self.assertIn("Task2", output)
        self.assertIn("high", output.lower())
        self.assertIn("low", output.lower())

if __name__ == "__main__":
    unittest.main()