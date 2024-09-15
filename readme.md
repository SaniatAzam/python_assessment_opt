# Task Management System

This is a simple command-line (CLI) task management system implemented in Python.

## Functional Requirements

The application should allow users to do the following:

1. Add a new task
2. Complete a task
3. List all tasks (with an option to show only incomplete tasks)
4. Generate a report of task statistics, which should include:
   - Total number of tasks
   - Number of completed tasks
   - Number of pending tasks
   - Average time taken to complete a task
5. The application must persist user data across sessions, ensuring that all information remains intact and accessible upon returning, without resetting or losing any previously entered tasks

## Setup

1. Ensure you have Python 3.7 or higher installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory in your terminal.
4. Install Poetry if you don't have it installed:
    ```
    curl -sSL https://install.python-poetry.org | python3 -
    ```
5. Install dependencies
    ```
    poetry install
    ```
6.  Running the application
    ```
    poetry run python main.py
    ```

## Running Tests

To run all the unit tests, use the following command:

```
python -m unittest discover tests
```

## Your Task

**Ensure and validate with tests that the app meets the required functionality** and addresses any bugs. Enhance performance and do optimisations to the best of your knowledge, while refactoring the code for better readability and maintainability. Feel free to make necessary assumptions where applicable.

## Submission

Once you are done, please:

1. Push your code to a **public** GitHub repository with at least **read** access
2. Reply to our email with the repository link to complete your submission within the deadline

Good luck!
