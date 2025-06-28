import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

import unittest
import json
from task_tracker_cli.models import Task

class TestTask(unittest.TestCase):
    
    def setUp(self):
        self.task1 = Task(_id=1, description='Test description for test task 1')

    def test_creates_dict(self):
        dict = self.task1.todict()
        self.assertEqual(dict['id'], self.task1.id)
        self.assertEqual(dict['description'], self.task1.description)
        self.assertEqual(dict['createdAt'], self.task1.createdAt.isoformat())
        self.assertEqual(dict['updatedAt'], self.task1.updatedAt.isoformat())
        self.assertEqual(dict['status'], self.task1.status.value)
    
    def test_reverses_dict_to_object(self):
        obj = Task.fromdict(self.task1.todict())
        self.assertEqual(obj.id, self.task1.id)
        self.assertEqual(obj.description, self.task1.description)
        self.assertEqual(obj.createdAt, self.task1.createdAt)
        self.assertEqual(obj.updatedAt, self.task1.updatedAt)
        self.assertEqual(obj.status, self.task1.status)

    def test_serializes_deserealizes(self):
        json_str = json.dumps(self.task1.todict())
        obj = Task.fromdict(json.loads(json_str))
        self.assertEqual(obj.id, self.task1.id)
        self.assertEqual(obj.description, self.task1.description)
        self.assertEqual(obj.createdAt, self.task1.createdAt)
        self.assertEqual(obj.updatedAt, self.task1.updatedAt)
        self.assertEqual(obj.status, self.task1.status)

if __name__ == '__main__':
    unittest.main()