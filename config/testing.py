import os

DEBUG = False
TESTING = True
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    os.path.dirname(__file__), "../data-test.sqlite3")
