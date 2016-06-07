import unittest
from app import create_app, db
from app.models import Result
import datetime

class ResultModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app_ctx.pop()

    def test_initialize_result(self):
        now = datetime.datetime.now()
        snapshot = {
            "timestamp": now,
            "download": 5.2,
            "upload": 1.3,
            "ping": 10.3,
            "result": "success",
        }
        result = Result(snapshot)
        self.assertEqual(result.timestamp, now)
        self.assertEqual(result.download, 5.2)
        self.assertEqual(result.upload, 1.3)
        self.assertEqual(result.ping, 10.3)
        self.assertEqual(result.result, "success")
