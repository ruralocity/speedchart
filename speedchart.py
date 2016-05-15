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
        # needs:
        # labels (timestamps)
        # data (ping/dl/ul speed)
        records = []
        labels = []
        download_speeds = []
        upload_speeds = []
        ping_speeds = []
        for file in os.listdir("data"):
            if file.endswith(".speedtest.txt"):
                records.append(self.parse("data/" + file))
        for record in records:
            labels.append(record["timestamp"])
            if record["result"] == "success":
                download_speeds.append(record["download"])
                upload_speeds.append(record["upload"])
                ping_speeds.append(record["ping"])
        datasets = [
            {
                "label": "Download Speed",
                "data": download_speeds,
                "fillColor": "rgba(100,90,205,0.1)",
                "strokeColor": "rgba(100,90,205,0.5)",
                "pointColor": "rgba(100,90,205,0.5)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(220,220,220,1)"
            },
            {
                "label": "Upload Speed",
                "data": upload_speeds,
                "fillColor": "rgba(151,187,205,0.2)",
                "strokeColor": "rgba(151,187,205,1)",
                "pointColor": "rgba(151,187,205,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(151,187,205,1)"
            },
            {
                "label": "Ping Speed",
                "data": ping_speeds,
                "fillColor":"rgba(220,220,220,0.2)",
                "strokeColor": "rgba(220,220,220,1)",
                "pointColor": "rgba(220,220,220,1)",
                "pointStrokeColor": "#fff",
                "pointHighlightFill": "#fff",
                "pointHighlightStroke": "rgba(151,187,205,1)"
            }
        ]
        summary = {}
        summary["labels"] = labels
        summary["datasets"] = datasets
        return summary

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
        # TODO: Revert parse_all to create standard dict, then convert data from
        # database into chart.js format.
        if Result.query.filter_by(timestamp=record["timestamp"]) is None:
            db.session.add(Result(record))
            db.session.commit()
        return record

@app.route("/")
def index():
    parser = Parser()
    data = parser.parse_all()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
