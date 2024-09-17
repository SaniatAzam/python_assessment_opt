from datetime import datetime


class Task:
    """
    A class to represent a task.

    Attributes:
            - title: str
                    title of the task
            - description: str
                    a description of the task
            - completed: bool
                    flag to check if the task is completed
            - created_at: datetime
                    time of task creation
            - completion_time: str | None
                    time taken for the task to be completed

    """

    def __init__(
        self,
        title: str,
        description: str,
        completed: bool = False,
        created_at: datetime = datetime.now(),
        completion_time: str | None = None,
    ):
        """Initializes a new task with the given parameters"""
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at
        self.completion_time = completion_time
