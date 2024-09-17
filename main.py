import argparse
from task_manager import TaskManager
from storage import Storage
from utils import create_data_file, update_data_file


# The application currently only supports JSON files
# Changing the extension to anything else will safely throw an error message

DATA_FILE = "./tasks.json"


def main():
    # Initialize a storage and access/create the JSON dataset that will persist
    storage = Storage()

    try:
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

        update_data_file(DATA_FILE, storage)

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
