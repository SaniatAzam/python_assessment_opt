import unittest
from unittest.mock import MagicMock
from storage import Storage
from task import Task
from utils import create_data_file, update_data_file
import os
from datetime import datetime

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
        last_directory = current_directory_tokens[cdt_length-1]

        self.test_file_directory = self.current_directory
        if last_directory != "tests":
            self.test_file_directory = os.path.join(self.current_directory, './tests')

    def test_valid_file_creation(self):
        test_file_name = "test_1.json"
        create_data_file(test_file_name, self.storage)
        self.assertTrue(os.path.exists(test_file_name))

        try:
            os.remove(test_file_name)
        except FileNotFoundError:
            pass

    def test_illegal_extension_file_creation(self):
        test_file_name = "faulty.xml"

        with self.assertRaises(ValueError):
            create_data_file(test_file_name, self.storage)

        self.assertFalse(os.path.exists(test_file_name))

    def test_storage_save_task(self):
        # test_file_name = "test_2.json"
        # create_data_file(test_file_name, self.storage)
        task = Task("Task 1", "Description 1")
        self.assertTrue(self.storage.save_task(task))
        task_list = self.storage.tasks.values()
        self.assertIn(task, task_list)

    def test_storage_save_duplicate_task(self):
        task_1 = Task("Task 1", "Description 1")
        self.assertTrue(self.storage.save_task(task_1))
        task_list = self.storage.tasks.values()
        self.assertIn(task_1, task_list)

        task_2 = Task("Task 1", "Different Description")
        self.assertFalse(self.storage.save_task(task_2))
        task_list = self.storage.tasks.values()
        self.assertNotIn(task_2, task_list)

    def test_storage_update_task(self):
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

    def test_storage_load_task_from_file_and_type_conversions(self):
        test_file_name = os.path.join(self.test_file_directory, 'load_test_1.json')
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
    def test_storage_load_multiple_tasks_from_file(self):
        test_file_name = os.path.join(self.test_file_directory, 'load_test_2.json')

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


if __name__ == "__main__":
    unittest.main()
