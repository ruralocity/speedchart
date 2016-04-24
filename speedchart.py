from flask import Flask, render_template
from parser import Parser
import json
app = Flask(__name__)

@app.route("/")
def index():
    parser = Parser()
    data = parser.parse_all()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
