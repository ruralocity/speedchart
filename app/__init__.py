import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    cfg = os.path.join(os.getcwd(), "config", config_name + ".py")
    app.config.from_pyfile(cfg)

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
