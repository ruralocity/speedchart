import os
import re
from . import db
from .models import Result
import datetime

class Parser(object):
    """Parse output from Speedtest CLI"""

    def parse_all(self):
        for file in os.listdir("data"):
            if file.endswith(".speedtest.txt"):
                self.parse("data/" + file)

    def parse(self, file):
        input = open(file, "r")
        data = input.read()
        input.close()

        timestamp = re.search(r'Speed Test Ran at:  (.*)', data)
        ping = re.search(r'Ping: (.*) ms', data)
        download = re.search(r'Download: (.*) Mbit/s', data)
        upload = re.search(r'Upload: (.*) Mbit/s', data)
        record = {}
        if timestamp:
            record["timestamp"] = datetime.datetime.strptime(timestamp.group(1), "%d/%m/%Y %H:%M")
            if ping:
                record["result"] = "success"
                record["ping"] = (float(ping.group(1)) / 100.0)
                record["download"] = download.group(1)
                record["upload"] = upload.group(1)
            else:
                record["result"] = "failure"
        if Result.query.filter_by(timestamp=record["timestamp"]).first() is None:
            db.session.add(Result(record))
            db.session.commit()
        return record

class Charter(object):
    """Structure data in Chart.js format"""

    def __init__(self):
        self.labels = []
        self.download_speeds = []
        self.upload_speeds = []
        self.ping_speeds = []
        # temporarily get all records from the database
        self.records = Result.query.order_by(Result.timestamp).all()
        for record in self.records:
            self.labels.append(record.timestamp)
            if record.result == "success":
                self.download_speeds.append(record.download)
                self.upload_speeds.append(record.upload)
                self.ping_speeds.append(record.ping)

    def output(self):
        datasets = [
            {
                "label": "Download Speed",
                "data": self.download_speeds,
                "fillColor": "rgba(100,90,205,0.1)",
                "strokeColor": "rgba(100,90,205,0.5)",
                "pointColor": "rgba(100,90,205,0.5)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(220,220,220,1)"
            },
            {
                "label": "Upload Speed",
                "data": self.upload_speeds,
                "fillColor": "rgba(151,187,205,0.2)",
                "strokeColor": "rgba(151,187,205,1)",
                "pointColor": "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(151,187,205,1)"
            },
            {
                "label": "Ping Speed",
                "data": self.ping_speeds,
                "fillColor":"rgba(220,220,220,0.2)",
                "strokeColor": "rgba(220,220,220,1)",
                "pointColor": "rgba(220,220,220,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(151,187,205,1)"
            }
        ]
        summary = {}
        summary["labels"] = self.labels
        summary["datasets"] = datasets
        return summary
