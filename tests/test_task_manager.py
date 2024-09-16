import unittest
from unittest.mock import MagicMock
from task_manager import TaskManager
from task import Task
from datetime import datetime, timedelta


class TestTaskManager(unittest.TestCase):
	def setUp(self):
		self.storage = MagicMock()
		self.manager = TaskManager(self.storage)
		self.test_date = datetime.fromisoformat("2024-09-15 17:26:07.461444")

	def test_add_new_task_successfully(self):
		self.storage.save_task.return_value = True
		response = self.manager.add_task("Test Task", "Description")
		self.assertTrue(response)

	def test_add_new_task_unsuccessfully(self):
		self.storage.save_task.return_value = False
		response = self.manager.add_task("Test Task", "Description")
		self.assertFalse(response)

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

	def test_generate_report_no_completed_tasks(self):
		tasks = [
			Task("Task 1", "Description 1"),
			Task("Task 2", "Description 2"),
			Task("Task 3", "Description 3")
		]
		self.storage.get_all_tasks.return_value = tasks
		report = self.manager.generate_report()
		self.assertEqual(report["total"], 3)
		self.assertEqual(report["completed"], 0)
		self.assertEqual(report["pending"], 3)

	def test_generate_report_one_completed_task(self):
		tasks = [
			Task("Task 1", "Description 1", True, self.test_date, "2:03:12.0"),
			Task("Task 2", "Description 2"),
			Task("Task 3", "Description 3")
		]
		expected_act = "02 hours - 03 minutes - 12 seconds"
		self.storage.get_all_tasks.return_value = tasks
		report = self.manager.generate_report()
		self.assertEqual(report["total"], 3)
		self.assertEqual(report["completed"], 1)
		self.assertEqual(report["pending"], 2)
		self.assertEqual(report["average completion time"], expected_act)

	def test_generate_report_average_completion_time(self):
		tasks = [
			Task("Task 1", "Description 1", True, self.test_date, "1:10:20.0"),
			Task("Task 2", "Description 2", True, self.test_date, "2:12:15.1"),
			Task("Task 3", "Description 3")
		]
		self.storage.get_all_tasks.return_value = tasks

		h1, m1, s1 = map(float, tasks[0].completion_time.split(":"))
		h2, m2, s2 = map(float, tasks[1].completion_time.split(":"))

		total_seconds = (timedelta(hours=h1, minutes=m1, seconds=s1) + timedelta(hours=h2, minutes=m2, seconds=s2)).total_seconds()

		avg_t_seconds = total_seconds / 2

		avg_h = int( avg_t_seconds // 3600)
		avg_m = int((avg_t_seconds % 3600) // 60)
		avg_s = int(avg_t_seconds % 60)

		expected_act = f"{avg_h:02} hours - {avg_m:02} minutes - {avg_s:02} seconds"

		report = self.manager.generate_report()

		self.assertEqual(report["total"], 3)
		self.assertEqual(report["completed"], 2)
		self.assertEqual(report["pending"], 1)
		self.assertEqual(report["average completion time"], expected_act)

	def test_complete_task(self):
		self.storage.get_task.return_value = Task("Task 1", "Description 1", created_at=self.test_date)
		result = self.manager.complete_task("Task 1")
		self.assertEqual(result, (True, 1))

	def test_complete_nonexistent_task(self):
		self.storage.get_task.return_value = None
		result = self.manager.complete_task("Non-existent Task")
		self.assertEqual(result, (False, -1))

	def test_complete_completed_task(self):
		test_task = Task("Completed Task", "Description 1", True, self.test_date, "1:10:20.0")
		self.storage.get_task.return_value = test_task
		result = self.manager.complete_task("Completed Task")
		self.assertEqual(result, (False, 1))


if __name__ == "__main__":
	unittest.main()
