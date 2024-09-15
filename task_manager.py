from datetime import datetime
from storage import Storage


class Task:

	def __init__(self, title, description):
		self.title = title
		self.description = description
		self.completed = False
		self.created_at = datetime.now().isoformat()


class TaskManager:

	def __init__(self, storage: Storage):
		self.storage = storage

	def add_task(self, title: str, description: str):
		task = Task(title, description)
		self.storage.save_task(task)
		return task

	def complete_task(self, title: str):
		task = self.storage.get_task(title)
		if task:
			task.completed = True
			self.storage.update_task(task)
			return True
		return False

	def list_tasks(self, include_completed: bool = False):
		tasks = self.storage.get_all_tasks()
		return tasks

	def generate_report(self):
		tasks = self.storage.get_all_tasks()
		total_tasks = len(tasks)
		completed_tasks = len([task for task in tasks if task.completed])

		report = {
		    "total": total_tasks,
		    "completed": completed_tasks,
		    "pending": total_tasks - completed_tasks
		}

		return report

