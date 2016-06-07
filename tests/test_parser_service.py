import unittest
from app import create_app, db
from app.services import Parser
from app.models import Result
import datetime

class ParserServiceTestCase(unittest.TestCase):
        def setUp(self):
            self.app = create_app("testing")
            self.app_ctx = self.app.app_context()
            self.app_ctx.push()
            db.create_all()

        def tearDown(self):
            db.drop_all()
            self.app_ctx.pop()

        def test_parse_single_successful_result(self):
            file = "testdata/testfile.speedtest.txt"
            parser = Parser()
            parsed = parser.parse(file)
            self.assertEqual(parsed["download"], "3.06")
            self.assertEqual(parsed["upload"], "1.01")
            self.assertEqual(parsed["timestamp"], datetime.datetime(2016, 3, 12, 15, 0))
            self.assertEqual(parsed["ping"], 1.6635499999999999)
            self.assertEqual(parsed["result"], "success")

        def test_persist_single_successful_result(self):
            file = "testdata/testfile.speedtest.txt"
            parser = Parser()
            parser.parse(file)
            results = Result.query.order_by(Result.timestamp).first()
            self.assertEqual(results.timestamp, datetime.datetime(2016, 3, 12, 15, 0))
            self.assertEqual(results.download, 3.06)
            self.assertEqual(results.upload, 1.01)
            self.assertEqual(results.ping, 1.6635499999999999)
            self.assertEqual(results.result, "success")
