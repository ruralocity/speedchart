from flask import render_template
from ..services import Parser, Charter
from . import main

@main.route("/")
def index():
    parser = Parser()
    parser.parse_all() # for now
    charter = Charter()
    data = charter.output()
    return render_template("index.html", data=data)
