import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

import unittest
from task_tracker_cli.models import Task, Status
import task_tracker_cli.repo_utils as ru
from task_tracker_cli.file_repo import JsonFileRepo

class TestFileRepo(unittest.TestCase):

    def setUp(self):
        ru._ID_POOL_PATH = 'test_id.json'
        ru._SAVE_FILE_PATH = 'test.json'
        self.repo = JsonFileRepo()

    def tearDown(self):
        if os.path.exists('test_id.json'):
            os.remove('test_id.json')
        if os.path.exists('test.json'):
            os.remove('test.json')

    def compare_task(self, task: Task):
        self.assertEqual(task.id, self.repo.tasks[task.id].id)
        self.assertEqual(task.description, self.repo.tasks[task.id].description)
        self.assertEqual(task.createdAt, self.repo.tasks[task.id].createdAt)
        self.assertEqual(task.updatedAt, self.repo.tasks[task.id].updatedAt)
        self.assertEqual(task.status, self.repo.tasks[task.id].status)

    def test_creates_tasks(self):
        self.repo.create('Test description for test task 1')
        self.repo.create('Test description for test task 2')
        self.repo.create('Test description for test task 3')
        self.repo.create('Test description for test task 4')

        from_file = ru.load_tasks()
        for task in from_file.values():
            self.compare_task(task)

    def test_updates_task_status(self):
        new_task1 = self.repo.create('Test task for updating status 1')
        new_task2 = self.repo.create('Test task for updating status 2')
        self.repo.set_status(new_task1.id, Status.DONE)
        self.repo.set_status(new_task2.id, Status.IN_PROGRESS)

        from_file = ru.load_tasks()
        self.assertEqual(from_file[1].status, Status.DONE)
        self.assertEqual(from_file[2].status, Status.IN_PROGRESS)
        self.assertNotEqual(from_file[1].updatedAt.isoformat(), from_file[1].createdAt.isoformat())

    def test_updates_task_description(self):
        new_task1 = self.repo.create('Test task for updating status 1')
        new_task2 = self.repo.create('Test task for updating status 2')
        self.repo.set_description(new_task1.id, 'New description 1')
        self.repo.set_description(new_task2.id, 'New description 2')

        from_file = ru.load_tasks()
        self.assertEqual(from_file[1].description, 'New description 1')
        self.assertEqual(from_file[2].description, 'New description 2')
        self.assertNotEqual(from_file[1].updatedAt.isoformat(), from_file[1].createdAt.isoformat())

    def gets_tasks(self):
        self.repo.create('Test task 1')
        self.repo.create('Test task 2')
        self.repo.create('Test task 3')
        self.repo = JsonFileRepo()
        self.repo.set_status(1, Status.IN_PROGRESS)
        self.repo.set_status(3, Status.IN_PROGRESS)
        
        self.assertEqual(self.repo.get_by_id(1).description, 'Test task 1')
        in_progress = self.repo.get_by_status(Status.IN_PROGRESS)
        for task in in_progress:
            self.assertEqual(task.status, Status.IN_PROGRESS)



if __name__ == '__main__':
    unittest.main()