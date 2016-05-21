from . import db

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
