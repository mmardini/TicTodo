import os
import unittest
import tempfile

import tictodo
from database import db_session
from models import Task, User
from tasks_api import tasks_get, tasks_post, task_put


class TasksAPITestCase(unittest.TestCase):
    def setUp(self):
        self.user1 = User("test-user1", "")
        self.user2 = User("test-user2", "")
        db_session.add(self.user1)
        db_session.add(self.user2)
        db_session.commit()

        self.task1 = Task("test-task1", 0, self.user1.id)
        self.task2 = Task("test-task2", 0, self.user2.id)
        db_session.add(self.task1)
        db_session.add(self.task2)
        db_session.commit()

    def tearDown(self):
        db_session.delete(self.user1)
        db_session.delete(self.task1)
        db_session.delete(self.user2)
        db_session.delete(self.task2)
        db_session.commit()

        task3 = Task.query.filter(Task.text == "test-task3").first()
        if task3 is not None:
            db_session.delete(task3)
            db_session.commit()

    def test_tasks_get(self):
        response = tasks_get(self.user1.id)
        # Get a response that has all tasks owned by the user.
        self.assertIn('"text": "test-task1"',
                      response.response[0])
        # But not other users' tasks.
        self.assertNotIn('"text": "test-task2"',
                         response.response[0])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

    def test_tasks_post(self):
        self.assertNotIn('"text": "test-task3"',
                         tasks_get(self.user1.id).response[0])

        tasks_post("test-task3", 0, self.user1.id)

        self.assertIn('"text": "test-task3"',
                      tasks_get(self.user1.id).response[0])

    def test_task_put(self):
        # User should be able to update his/her tasks.
        response1 = task_put(self.task1.id, self.user1.id, order=10)
        self.assertEqual(response1.status_code, 204)

        # But should be unable to update other users' tasks.
        response2 = task_put(self.task2.id, self.user1.id, order=10)
        self.assertEqual(response2.status_code, 403)

if __name__ == '__main__':
    unittest.main()
