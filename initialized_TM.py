from task_manager import TaskManager
from storage import Storage


storage = Storage()
m = TaskManager(storage)


class InitializedTaskManager:
    def __init__(self):
        self.manager = m

