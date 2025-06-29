import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

import unittest
import json
import task_tracker_cli.repo_utils as ru
from task_tracker_cli.models import Task

class TestRepoUtils(unittest.TestCase):

    def setUp(self):
        self.tasks = [
            Task(1, 'Test description 1'),
            Task(2, 'Test description 2'),
            Task(3, 'Test description 3'),
            Task(4, 'Test description 4'),
            Task(5, 'Test description 5')
        ]

        ru._SAVE_FILE_PATH = 'test.json'
        ru._ID_POOL_PATH = 'test_id.json'

    def tearDown(self):
        if os.path.exists('test.json'):
            os.remove('test.json')
        if os.path.exists('test_id.json'):
            os.remove('test_id.json')

    def test_saves_loads_tasks_simple(self):
        ru.save_tasks(self.tasks)
        loaded = ru.load_tasks()

        i = 0
        for task in loaded.values():
            self.assertEqual(self.tasks[i].id, task.id)
            self.assertEqual(self.tasks[i].description, task.description)
            self.assertEqual(self.tasks[i].createdAt, task.createdAt)
            self.assertEqual(self.tasks[i].updatedAt, task.updatedAt)
            self.assertEqual(self.tasks[i].status, task.status)
            i += 1

    def test_loads_tasks_with_no_file(self):
        loaded = ru.load_tasks()
        self.assertIsInstance(loaded, dict)
        self.assertEqual(len(loaded), 0)

    def test_loads_tasks_with_empty_file(self):
        with open(ru._SAVE_FILE_PATH, 'w'):
            pass
        loaded = ru.load_tasks()
        self.assertIsInstance(loaded, dict)
        self.assertEqual(len(loaded), 0)

        with open(ru._SAVE_FILE_PATH, 'w') as file:
            file.write('{ }')
        loaded = ru.load_tasks()
        self.assertIsInstance(loaded, dict)
        self.assertEqual(len(loaded), 0)

        with open(ru._SAVE_FILE_PATH, 'w') as file:
            file.write('[ ]')
        loaded = ru.load_tasks()
        self.assertIsInstance(loaded, dict)
        self.assertEqual(len(loaded), 0)
    
    def test_loads_tasks_with_invalid_file(self):
        with open(ru._SAVE_FILE_PATH, 'w') as file:
            file.write(' ')
        self.assertRaises(json.JSONDecodeError, ru.load_tasks)

        with open(ru._SAVE_FILE_PATH, 'w') as file:
            file.write('{ ')
        self.assertRaises(json.JSONDecodeError, ru.load_tasks)
    
    def test_saves_with_invalid_file(self):
        with open(ru._SAVE_FILE_PATH, 'w') as file:
            file.write('invalid json')
        ru.save_tasks(self.tasks)
        loaded = ru.load_tasks()

        i = 0
        for task in loaded.values():
            self.assertEqual(self.tasks[i].id, task.id)
            self.assertEqual(self.tasks[i].description, task.description)
            self.assertEqual(self.tasks[i].createdAt, task.createdAt)
            self.assertEqual(self.tasks[i].updatedAt, task.updatedAt)
            self.assertEqual(self.tasks[i].status, task.status)
            i += 1
    
    def test_generates_id(self):
        first = ru.generate_id()
        pool = ru._load_id_pool()
        self.assertEqual(first, 1)
        self.assertEqual(len(pool['taken']), 1)
        self.assertEqual(len(pool['reuse']), 0)
        self.assertEqual(pool['taken'][0], first)

        second = ru.generate_id()
        pool = ru._load_id_pool()
        self.assertEqual(second, 2)
        self.assertEqual(len(pool['taken']), 2)
        self.assertEqual(len(pool['reuse']), 0)
        self.assertEqual(pool['taken'][0], first)
        self.assertEqual(pool['taken'][1], second)

        third = ru.generate_id()
        pool = ru._load_id_pool()
        self.assertEqual(third, 3)

        ru.release_id(2)
        pool = ru._load_id_pool()
        self.assertEqual(len(pool['taken']), 2)
        self.assertEqual(len(pool['reuse']), 1)
        self.assertEqual(pool['reuse'][0], 2)

        ru.release_id(3)
        fourth = ru.generate_id()
        self.assertEqual(fourth, 2)
        fifth = ru.generate_id()
        self.assertEqual(fifth, 3)
        sixth = ru.generate_id()
        self.assertEqual(sixth, 4)

if __name__ == '__main__':
    unittest.main()