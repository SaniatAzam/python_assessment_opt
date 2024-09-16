import datetime
import json
from task import Task
from datetime import datetime
# from main import DATA_FILE


class Storage:
	"""
	A class to handle storage, retrieval, and manipulation of tasks.

	Attributes:
		- tasks: list[Task]
			the list of all the tasks that have been added to storage

	"""

	def __init__(self):
		""" Initializes a new storage with an empty list of tasks. """
		self.tasks: list[Task] = []

	def save_task(self, task: Task) -> bool:
		"""
		Adds a new task to the storage
		Parameters:
		- task: Task
			the task to be added

		Returns:
			- True: bool
				if the save was successful
			- False: bool
				if there is an existing task with matching titles
		"""
		already_exists = False
		for _, t in enumerate(self.tasks):
			if t.title == task.title:
				already_exists = True
				break

		if not already_exists:
			self.tasks.append(task)
			return True
		else:
			return False

	def update_task(self, updated_task: Task) -> None:
		"""
		Updates an existing task in the storage.

		Parameters:
			- updated_task: Task
				the task with the updated details

		Returns:
			- None
		"""
		for i, task in enumerate(self.tasks):
			if task.title == updated_task.title:
				self.tasks[i] = updated_task
				break

	def load_tasks(self, f) -> None:
		"""
		Loads tasks from a file into the storage.

		Parameters:
			- f: file object
				the file to read tasks from in JSON format

		Returns:
			- None
		"""

		f.seek(0)
		tasks = json.load(f)

		for task in tasks:
			title = task.get("title")
			description = task.get("description")
			completed = task.get("completed")
			created_at = datetime.fromisoformat((task.get("created_at")))
			completion_time = task.get("completion_time") if task.get("completion_time") else None
			fetched_task = Task(title, description, completed, created_at, completion_time)
			self.save_task(fetched_task)

	def dump(self, f) -> None:
		""" Formats each task into JSON and dumps all of it into a JSON file.

		Parameters:
			- f: file object
				a file object to write the tasks in JSON format

		Returns:
			- None
		"""
		serializable_tasks_list = []
		try:
			for t in self.tasks:
				task = {
					"title": t.title,
					"description": t.description,
					"completed": t.completed,
					"created_at": str(t.created_at),
					"completion_time": str(t.completion_time) if t.completion_time else None
				}
				serializable_tasks_list.append(task)

			json.dump(serializable_tasks_list, f, indent=4)
		except Exception as e:
			print(f"Failed to dump tasks to file: {e}")

	def get_task(self, title: str) -> Task | None:
		""" Fetches a task by its title

		Parameters:
			- title: str
				title of the task to be fetched

		Returns:
			- Task | None
				Task object if found else None
		"""
		for task in self.tasks:
			if task.title == title:
				return task
		return None

	def get_all_tasks(self) -> list[Task]:
		""" Returns the list of all the tasks in the storage's list.

		Returns:
			list[Tasks]
		"""
		return list(self.tasks)

	def clear_all_tasks(self):
		"""Clears all task from storage."""
		self.tasks = []
		# try:
		# 	with open(DATA_FILE, "w") as f:
		# 		f.write("")
		# except EOFError:
		# 	pass


