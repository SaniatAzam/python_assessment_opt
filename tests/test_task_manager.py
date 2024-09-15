import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from task_manager import Task, TaskManager


class TestTaskManager(unittest.TestCase):

	def setUp(self):
		self.storage = MagicMock()
		self.manager = TaskManager(self.storage)

	def test_add_task(self):
		task = self.manager.add_task("Test Task", "Description")
		self.storage.save_task.assert_called_once()
		self.assertEqual(task.title, "Test Task")
		self.assertEqual(task.description, "Description")

	def test_list_tasks_exclude_completed(self):
		tasks = [
			Task("Task 1", "Description 1"),
			Task("Task 2", "Description 2"),
			Task("Task 3", "Description 3")
		]
		tasks[1].completed = True
		self.storage.get_all_tasks.return_value = tasks
		result = self.manager.list_tasks()
		self.assertEqual(len(result), 2)
		self.assertNotIn(tasks[1], result)

	def test_generate_report(self):
		tasks = [
			Task("Task 1", "Description 1"),
			Task("Task 2", "Description 2"),
			Task("Task 3", "Description 3")
		]
		tasks[0].completed = True
		self.storage.get_all_tasks.return_value = tasks
		report = self.manager.generate_report()
		self.assertEqual(report["total"], 3)
		self.assertEqual(report["completed"], 2)
		self.assertEqual(report["pending"], 1)

	def test_complete_nonexistent_task(self):
		self.storage.get_task.return_value = None
		result = self.manager.complete_task("Non-existent Task")
		self.assertFalse(result)


if __name__ == "__main__":
	unittest.main()
