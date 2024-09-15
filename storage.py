class Storage:

	def __init__(self):
		self.tasks = []

	def save_task(self, task):
		self.tasks.append(task)

	def update_task(self, updated_task):
		for i, task in enumerate(self.tasks):
			if task.title == updated_task.title:
				self.tasks[i] = updated_task
				break

	def load_tasks(self, t):
		pass



	def get_task(self, title):
		for task in self.tasks:
			if task.title == title:
				return task
		return None

	def get_all_tasks(self):
		return list(self.tasks)

	def clear_all_tasks(self):
		self.tasks = []
