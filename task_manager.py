from storage import Storage
from task import Task
from datetime import datetime, timedelta


class TaskManager:
    """
    A class to manage and manipulate tasks along with handling a storage.

    Assumption:
        - A user can not add a task that has been completed already.

    Attributes:
        - storage: Storage
            the main Storage object the class manages
    """

    def __init__(self, storage: Storage):
        """Initialized a new TaskManager with a given Storage object."""
        self.storage = storage

    def add_task(self, title: str, description: str):
        """
        Adds a new task to the storage with a given title and description.
        Returns the True if task was added successfully, and vice versa.

        Parameters:
            - title: str
                the title of the new task
            - description: str
                the description of the new task

        Returns:
            -True: bool
                if the task could be added to the storage
            -False: bool
                if the task could not be added to the storage

        """
        task = Task(title, description)
        saved = self.storage.save_task(task)
        return saved

    def complete_task(self, title: str) -> (bool, int):
        """
        Retrieves a task with the specified title from storage. Updates the tasks completion_time attribute.
        Returns a boolean indicating the success status of the function.

        Parameters:
            - title: str
                the title of the Task object to be found from storage

        Returns:
            - True: bool
                if the Task was found and updated accordingly
            - False: bool
                if the Task does not exist in storage
        """

        task = self.storage.get_task(title)

        if task:
            if task.completed:
                return False, 1

            task.completed = True

            # The approximate timestamp for when the task was declared to be completed.
            completed_at = datetime.fromisoformat(datetime.now().isoformat())
            created_at = task.created_at

            # The approximate time taken for the task to be completed calculated using the differences between when
            # it was completed and when it was created.
            time_taken = completed_at - created_at

            # The completion time is updated from None to the time taken.
            task.completion_time = time_taken
            self.storage.update_task(task)
            return True, 1
        return False, -1

    def list_tasks(self, include_completed: bool = False) -> list[Task] | None:
        """
        Retrieves all the tasks and returns either that or just the subset of the pending tasks.

        Paremeters:
            include_completed: bool = False (default)
                the flag that checks if we want all or just the pending tasks

        Returns:
            A list of Tasks
        """
        if include_completed:
            return self.storage.get_all_tasks()
        else:
            return [task for task in self.storage.get_all_tasks() if not task.completed]

    def generate_report(self) -> dict[str, (int | str)]:
        """
        Generates a report containing the total number of tasks, the number of completed tasks and the number of
        pending tasks. Additionally, if there is one or more completed tasks the report also includes the
        average completion time.
        """

        tasks = self.storage.get_all_tasks()
        total_tasks = len(tasks)
        completed_tasks = len([task for task in tasks if task.completed])
        completion_times_list = [
            task.completion_time for task in tasks if task.completed
        ]

        if completed_tasks > 0:
            total_completion_times = timedelta()

            for completion_time in completion_times_list:
                h, m, s = map(float, completion_time.split(":"))
                total_completion_times += timedelta(hours=h, minutes=m, seconds=s)

            total_completion_seconds = total_completion_times.total_seconds()

            avg_completion_seconds = total_completion_seconds / completed_tasks
            avg_hours = int(avg_completion_seconds // 3600)
            avg_minutes = int((avg_completion_seconds % 3600) // 60)
            avg_seconds = int(avg_completion_seconds % 60)

            avg_completion_time = f"{avg_hours:02} hours - {avg_minutes:02} minutes - {avg_seconds:02} seconds"

            report = {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": total_tasks - completed_tasks,
                "average completion time": avg_completion_time,
            }
        else:
            report = {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": total_tasks - completed_tasks,
            }

        return report
