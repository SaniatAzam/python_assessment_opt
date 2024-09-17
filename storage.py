import datetime
import json
from task import Task
from datetime import datetime


class Storage:
    """
    A class to handle storage, retrieval, and manipulation of tasks.

    Attributes:
            - tasks: dict[str, Task]
                    the dictionary of all the tasks that have been added to storage

    """

    def __init__(self):
        """Initializes a new storage with an empty dictionary of tasks."""
        self.tasks: dict[str, Task] = {}

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
        if task.title not in self.tasks.keys():
            self.tasks[task.title] = task
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
        self.tasks[updated_task.title] = updated_task

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
            completion_time = (
                task.get("completion_time") if task.get("completion_time") else None
            )

            # Bad Data Checks
            logic_1 = completed and completion_time is None
            logic_2 = not completed and completion_time is not None
            logic_3 = title is None
            logic_4 = description is None
            logic_5 = created_at is None
            logic_6 = completed and completion_time is None

            # Weed out illogical task objects
            if logic_1 or logic_2 or logic_3 or logic_4 or logic_5 or logic_6:
                raise ValueError(
                    "*** One or a few tasks in the data file have logical issues. **** "
                    "\n -   Please check if any of the tasks has missing field(s). "
                    "\n -   OR if there are logical errors such tasks stating they are completed and have "
                    "no completion time, and vice versa."
                )
            else:
                fetched_task = Task(
                    title, description, completed, created_at, completion_time
                )
                self.save_task(fetched_task)

    def dump(self, f) -> None:
        """Formats each task into JSON and dumps all of it into a JSON file.

        Parameters:
                - f: file object
                        a file object to write the tasks in JSON format

        Returns:
                - None
        """
        serializable_tasks_list = []
        try:
            for t in self.tasks.values():
                task = {
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "created_at": t.created_at.isoformat(),
                    "completion_time": (
                        str(t.completion_time) if t.completion_time else None
                    ),
                }
                serializable_tasks_list.append(task)

            json.dump(serializable_tasks_list, f, indent=4)
        except Exception as e:
            print(f"Failed to dump tasks to file: {e}")

    def get_task(self, title: str) -> Task | None:
        """Fetches a task by its title

        Parameters:
                - title: str
                        title of the task to be fetched

        Returns:
                - Task | None
                        Task object if found else None
        """
        if title in self.tasks.keys():
            return self.tasks[title]
        return None

    def get_all_tasks(self) -> list[Task]:
        """Returns the list of all the tasks in the storage's list.

        Returns:
                list[Tasks]
        """
        return list(self.tasks.values())
