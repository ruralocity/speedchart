from flask import Flask, render_template
import json
import os
import re
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.sqlite3"
db = SQLAlchemy(app)

class Result(db.Model):
    """Parsed Speedtest results"""
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, unique=True)
    download = db.Column(db.Float)
    upload = db.Column(db.Float)
    ping = db.Column(db.Float)
    result = db.Column(db.String)

    def __init__(self, dictionary):
        print dictionary
        for key in dictionary:
            setattr(self, key, dictionary[key])
        print self

class Parser(object):
    """Parse output from Speedtest CLI into JSON"""

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
            record["timestamp"] = timestamp.group(1)
            if ping:
                record["result"] = "success"
                record["ping"] = (float(ping.group(1)) / 100.0)
                record["download"] = download.group(1)
                record["upload"] = upload.group(1)
            else:
                record["result"] = "failure"
        if Result.query.filter_by(timestamp=record["timestamp"]) is None:
            db.session.add(Result(record))
            db.session.commit()
        return record

class Charter(object):
    """Format data in Chart.js JSON format"""

    def __init__(self):
        self.labels = []
        self.download_speeds = []
        self.upload_speeds = []
        self.ping_speeds = []
        # temporarily get all records from the database
        self.records = Result.query.all()
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

@app.route("/")
def index():
    parser = Parser()
    parser.parse_all() # for now
    charter = Charter()
    data = charter.output()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
