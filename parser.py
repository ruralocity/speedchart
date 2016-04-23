import os
import re

class Parser(object):
    """Parse output from Speedtest CLI into JSON"""

    def parse_all(self):
        # needs:
        # labels (timestamps)
        # data (ping/dl/ul speed)
        records = []
        labels = []
        download_speeds = []
        for file in os.listdir("data"):
            if file.endswith(".speedtest.txt"):
                records.append(self.parse("data/" + file))
        for record in records:
            labels.append(record["timestamp"])
            if record["result"] == "success":
                download_speeds.append(record["download"])
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
        ping = re.search(r'Ping: (.*)', data)
        download = re.search(r'Download: (.*) Mbit/s', data)
        upload = re.search(r'Upload: (.*)', data)
        record = {}
        if timestamp:
            record["timestamp"] = timestamp.group(1)
            if ping:
                record["result"] = "success"
                record["ping"] = ping.group(1)
                record["download"] = download.group(1)
                record["upload"] = upload.group(1)
            else:
                record["result"] = "failure"
        return record

if __name__ == "__main__":
    parser = Parser()
    print parser.parse_all()
