import os
import re
import json

class Parser(object):
    """Parse output from Speedtest CLI into JSON"""

    def parse_all(self):
        records = []
        for file in os.listdir("data"):
            if file.endswith(".speedtest.txt"):
                records.append(self.parse("data/" + file))
        return json.dumps(records)

    def parse(self, file):
        input = open(file, "r")
        data = input.read()
        input.close()

        timestamp = re.search(r'Speed Test Ran at:  (.*)', data)
        ping = re.search(r'Ping: (.*)', data)
        download = re.search(r'Download: (.*)', data)
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

parser = Parser()
print parser.parse_all()
