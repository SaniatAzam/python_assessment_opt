import unittest
from storage import Storage
from task import Task
from utils import create_data_file, update_data_file
import os
from datetime import datetime
import json


# Due to the symbiotic relationship between the persistent data and the storage class,
# I decided to keep the tests in one test case.


class TestStorageDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = Storage()

        # Discovered the main command line to run all tests does not work because of directory mismatch
        # Setting up directory changes in those cases
        self.current_directory = os.getcwd()
        current_directory_tokens = self.current_directory.split("/")
        cdt_length = len(current_directory_tokens)
        last_directory = current_directory_tokens[cdt_length - 1]

        self.test_file_directory = self.current_directory
        if last_directory != "tests":
            self.test_file_directory = os.path.join(self.current_directory, "./tests")

    def test_valid_file_creation(self) -> None:
        test_file_name = "test_1.json"
        create_data_file(test_file_name, self.storage)
        self.assertTrue(os.path.exists(test_file_name))

        try:
            os.remove(test_file_name)
        except FileNotFoundError:
            pass

    def test_illegal_extension_file_creation(self) -> None:
        test_file_name = "faulty.xml"

        with self.assertRaises(ValueError):
            create_data_file(test_file_name, self.storage)

        self.assertFalse(os.path.exists(test_file_name))

    def test_storage_save_task(self) -> None:
        # test_file_name = "test_2.json"
        # create_data_file(test_file_name, self.storage)
        task = Task("Task 1", "Description 1")
        self.assertTrue(self.storage.save_task(task))
        task_list = self.storage.tasks.values()
        self.assertIn(task, task_list)

    def test_storage_save_duplicate_task(self) -> None:
        task_1 = Task("Task 1", "Description 1")
        self.assertTrue(self.storage.save_task(task_1))
        task_list = self.storage.tasks.values()
        self.assertIn(task_1, task_list)

        task_2 = Task("Task 1", "Different Description")
        self.assertFalse(self.storage.save_task(task_2))
        task_list = self.storage.tasks.values()
        self.assertNotIn(task_2, task_list)

    def test_storage_get_task(self) -> None:
        task_1 = Task(
            "Get Task 1",
            "Get Task 1 Desc",
            False,
            datetime.fromisoformat("2024-09-16T17:19:22.056316"),
            None,
        )
        task_2 = Task(
            "Get Task 2",
            "Get Task 2 Desc",
            True,
            datetime.fromisoformat("2024-06-10T17:19:22.056316"),
            "0:03:12.057624",
        )
        self.storage.tasks = {task_1.title: task_1, task_2.title: task_2}

        fetched_task = self.storage.get_task(task_1.title)

        self.assertEqual(fetched_task, task_1)

    def test_storage_get_nonexistent_task(self) -> None:
        task_1 = Task(
            "Get Task 1",
            "Get Task 1 Desc",
            False,
            datetime.fromisoformat("2024-09-16T17:19:22.056316"),
            None,
        )
        self.storage.tasks = {
            task_1.title: task_1,
        }

        fetched_task = self.storage.get_task("Ghost Task")

        self.assertIsNone(fetched_task)

    def test_storage_get_all_tasks(self) -> None:
        task_1 = Task(
            "Get Task 1",
            "Get Task 1 Desc",
            False,
            datetime.fromisoformat("2024-09-16T17:19:22.056316"),
            None,
        )
        task_2 = Task(
            "Get Task 2",
            "Get Task 2 Desc",
            True,
            datetime.fromisoformat("2024-06-10T17:19:22.056316"),
            "0:03:12.057624",
        )

        task_3 = Task("Get Task 3", "Get Task 3 Desc")

        self.storage.tasks = {
            task_1.title: task_1,
            task_2.title: task_2,
            task_3.title: task_3,
        }

        fetched_tasks_list = self.storage.get_all_tasks()
        direct_tasks_list = self.storage.tasks.values()

        for task in direct_tasks_list:
            self.assertIn(task, fetched_tasks_list)

    def test_storage_update_task(self) -> None:
        # Create a task
        task_1 = Task("Task 1", "Description 1")

        # Should successfully save the task
        self.assertTrue(self.storage.save_task(task_1))
        task_list = self.storage.tasks.values()

        # The task should be in the task list
        self.assertIn(task_1, task_list)

        # Initially the Task should not be completed, this wasn't necessary as we arent focusing on the Task class here
        self.assertFalse(task_1.completed)

        # Change the task's completion status to True
        task_1.completed = True

        # Get the actual dictionary from storage
        task_dict = self.storage.tasks

        # Update the task in storage (finally)
        self.storage.update_task(task_1)

        # The title should be in the dict and the completed should be True
        self.assertIn(task_1.title, task_dict.keys())
        self.assertTrue(task_dict[task_1.title].completed)

    def test_storage_load_task_from_file_and_type_conversions(self) -> None:
        test_file_name = os.path.join(self.test_file_directory, "load_test_1.json")
        creation_date_expected = datetime.fromisoformat("2024-09-16T17:19:22.056316")
        task_title_expected = "Load Test Task"
        description_expected = "Check Desc"

        # The test file should ideally be always there, so we are not doing any try-except blocks
        with open(test_file_name, "r") as f:
            self.storage.load_tasks(f)

        tasks_dict = self.storage.tasks

        self.assertIn(task_title_expected, tasks_dict.keys())

        # Dereferencing all the attributes, equating them to the expectations and making sure the types are okay.

        task_found = tasks_dict[task_title_expected]

        creation_date_found = task_found.created_at
        self.assertEqual(creation_date_found, creation_date_expected)
        self.assertIsInstance(creation_date_found, datetime)

        description_date_found = task_found.description
        self.assertEqual(description_date_found, description_expected)
        self.assertIsInstance(description_date_found, str)

        completion_status_found = task_found.completed
        self.assertFalse(completion_status_found)

        completion_time_found = task_found.completion_time
        self.assertIsNone(completion_time_found)
        self.assertIsInstance(completion_time_found, str | None)

    # More of a proof by induction, where we saw that it works for one task data,
    # so if works for 2 -- it should work for multiple
    def test_storage_load_multiple_tasks_from_file(self) -> None:
        test_file_name = os.path.join(self.test_file_directory, "load_test_2.json")

        # Expected Task 1
        creation_date_expected_1 = datetime.fromisoformat("2024-09-16T17:19:22.056316")
        task_title_expected_1 = "Load Test Task"
        description_expected_1 = "Check Desc"

        # Expected Task 2
        creation_date_expected_2 = datetime.fromisoformat("2024-06-10T17:19:22.056316")
        task_title_expected_2 = "Load Test Task 2"
        description_expected_2 = "Check Desc 2"
        completion_time_expected_2 = "0:03:12.057624"

        # The test file should ideally be always there, so we are not doing any try-except blocks
        with open(test_file_name, "r") as f:
            self.storage.load_tasks(f)

        tasks_dict = self.storage.tasks

        # Check if both the titles are in the keys list of the storage dict
        self.assertIn(task_title_expected_1, tasks_dict.keys())
        self.assertIn(task_title_expected_2, tasks_dict.keys())

        # Dereferencing all the attributes and equating them to the expected values
        task_found_1 = tasks_dict[task_title_expected_1]
        task_found_2 = tasks_dict[task_title_expected_2]

        creation_date_found_1 = task_found_1.created_at
        creation_date_found_2 = task_found_2.created_at
        self.assertEqual(creation_date_found_1, creation_date_expected_1)
        self.assertEqual(creation_date_found_2, creation_date_expected_2)

        description_date_found_1 = task_found_1.description
        description_date_found_2 = task_found_2.description
        self.assertEqual(description_date_found_1, description_expected_1)
        self.assertEqual(description_date_found_2, description_expected_2)

        completion_status_found_1 = task_found_1.completed
        completion_status_found_2 = task_found_2.completed
        self.assertFalse(completion_status_found_1)
        self.assertTrue(completion_status_found_2)

        completion_time_found_1 = task_found_1.completion_time
        completion_time_found_2 = task_found_2.completion_time
        self.assertIsNone(completion_time_found_1)
        self.assertEqual(completion_time_found_2, completion_time_expected_2)

    def test_storage_load_task_from_file_containing_bad_data(self) -> None:
        test_file_name = os.path.join(self.test_file_directory, "load_test_3.json")

        # We are going to try and load the data to storage, but it should throw a Value Error for having bad data
        with open(test_file_name, "r") as f:
            with self.assertRaises(ValueError):
                self.storage.load_tasks(f)

    # Gotta add tests for dumping
    def test_storage_dump_to_file(self) -> None:
        test_file_name_main = os.path.join(self.test_file_directory, "dump_test_1.json")
        test_file_name_check = os.path.join(self.test_file_directory, "dump_test_1_gold.json")
        task_1 = Task(
            "Dump Task 1",
            "Dump Task 1 Desc",
            False,
            datetime.fromisoformat("2024-09-16T17:19:22.050000"),
            None,
        )
        task_2 = Task(
            "Dump Task 2",
            "Dump Task 2 Desc",
            True,
            datetime.fromisoformat("2024-06-10T17:19:22.056316"),
            "0:03:12.057624",
        )
        self.storage.tasks = {task_1.title: task_1, task_2.title: task_2}

        # Dumping it to dump_test_1.json
        with open(test_file_name_main, "w") as f:
            self.storage.dump(f)

        # The files dump_test_1.json should have identical data to load_test_2.json
        # Load data from both the files

        dumped_file_data = None
        with open(test_file_name_main, "r") as f_dumped:
            dumped_file_data = json.load(f_dumped)

        gold_file_data = None
        with open(test_file_name_check, "r") as f_gold:
            gold_file_data = json.load(f_gold)

        self.assertEqual(dumped_file_data, gold_file_data)

        # We are going to reset dump_test_1.json to be empty now.
        # Optionally you can comment this out to check if the data is actually being
        # dumped to the dump test file.
        with open(test_file_name_main, "w") as f_dumped:
            pass

    def test_update_data_file(self) -> None:
        test_file_name_main = os.path.join(self.test_file_directory, "update_test_1.json")
        test_file_name_check = os.path.join(self.test_file_directory, "update_test_1_gold.json")
        task_1 = Task(
            "Update Task 1",
            "Update Task 1 Desc",
            False,
            datetime.fromisoformat("2024-09-16T17:19:22.056316"),
            None,
        )
        task_2 = Task(
            "Update Task 2",
            "Update Task 2 Desc",
            False,
            datetime.fromisoformat("2024-06-10T17:19:22.056316"),
            None,
        )
        self.storage.tasks = {task_1.title: task_1, task_2.title: task_2}

        # Dumping it to update_test_1.json
        with open(test_file_name_main, "w") as f:
            self.storage.dump(f)

        # We are going to try and update the tasks in storage by completing task 2 and then updating the file
        fetched_task_2 = self.storage.tasks["Update Task 2"]

        fetched_task_2.completed = True
        fetched_task_2.completion_time = "0:03:12.057624"

        update_data_file(test_file_name_main, self.storage)

        with open(test_file_name_main, "r") as f_updated:
            updated_file_data = json.load(f_updated)

        with open(test_file_name_check, "r") as f_gold:
            gold_file_data = json.load(f_gold)

        # The files should have the updated task
        self.assertEqual(updated_file_data, gold_file_data)

        # Revert the updates from file
        fetched_task_2.completed = False
        fetched_task_2.completion_time = None
        with open(test_file_name_main, "w") as f:
            self.storage.dump(f)


if __name__ == "__main__":
    unittest.main()
