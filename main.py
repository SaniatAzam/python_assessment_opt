import argparse
from task_manager import TaskManager
from storage import Storage


# The database is going to be a JSON file populated with an array of JSON Task objects.
DATA_FILE = "./tasks2.json"


def create_data_file(data_file: str, store: Storage) -> None:
    """
    Accesses the JSON file and loads the data into the Storage object. If the file doesn't exist, it creates it.

    Assumptions:
        - There are no Task objects to be loaded to the Storage object if the JSON Dataset does not exist in the first place.

    Parameters:
        - data_file: str
            file path
        - store: Storage
            storage object

    Returns:
        - None
    """

    try:
        with open(data_file, "r") as f:
            # Case where the file exists but there is no data.
            if f.read(1) == '':
                raise FileNotFoundError
            else:
                store.load_tasks(f)
    except FileNotFoundError:
        with open(data_file, "w") as f:
            f.write("[]")


def main():
    # Initialize a storage and access/create the JSON dataset that will persist
    storage = Storage()

    create_data_file(DATA_FILE, storage)

    # Initialize the TaskManager with the storage
    manager = TaskManager(storage)

    parser = argparse.ArgumentParser(description="Task Management System")
    subparsers = parser.add_subparsers(dest="command",
                                       help="Available commands")

    # Add task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("description", help="Task description")

    # Complete task
    complete_parser = subparsers.add_parser("complete",
                                            help="Mark a task as completed")
    complete_parser.add_argument("title", help="Task title")

    # List tasks
    list_parser = subparsers.add_parser("list", help="List incomplete tasks")
    list_parser.add_argument("--p",
                             action="store_false",
                             help="Shows only pending tasks")

    # Generate report
    subparsers.add_parser("report", help="Generate a report")

    args = parser.parse_args()

    if args.command == "add":
        successful = manager.add_task(args.title, args.description)
        conflict_msg = f"This title already exists for a task. Please select another title with the description: '{args.description}'"
        if not successful:
            print(conflict_msg)
        else:
            print(f"Task: '{args.title}' added successfully.")
    elif args.command == "complete":
        response = manager.complete_task(args.title)
        if response == (True, 1):
            print(f"Task '{args.title}' marked as completed.")
        elif response == (False, -1):
            print(f"Task '{args.title}' not found.")
        else:
            print(f"Task '{args.title}' has already been marked as completed before.")
    elif args.command == "list":
        tasks = manager.list_tasks(include_completed=args.p)
        checking_pending = args.p
        pending_string_modifier = "pending" if not checking_pending else ""
        if tasks:
            for task in tasks:
                status = "Completed" if task.completed else "Pending"
                print(f"{task.title} - {status}")
        else:
            print(f"No {pending_string_modifier} tasks found.")
    elif args.command == "report":
        print(manager.generate_report())
    else:
        parser.print_help()

    try:
        with open(DATA_FILE, "w") as f:
            storage.dump(f)
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    main()
