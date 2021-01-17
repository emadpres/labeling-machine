import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.template_folder = os.path.abspath('./frontend/templates')
app.static_folder = os.path.abspath('./frontend/static')
app.secret_key = "DOC_PATTERN_LABELING_KEY"

## SQLite Database
db_path = os.path.join(os.path.dirname(__file__), '../db/app.sqlite')
Path(db_path).parent.mkdir(parents=True, exist_ok=True)
db_uri = 'sqlite:///{}'.format(db_path)  # sqlite:////absolute/path/to/foo.db
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_ECHO'] = False  # Set this configuration to True if you want to see all of the SQL generated.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress this warning
db = SQLAlchemy(app)


# Why imported at very end?
# The bottom import is a workaround to circular imports, a common problem with Flask applications.
# route.py needs to import the 'app' variable defined in this script, so putting one of the reciprocal imports at
# the bottom avoids the error that results from the mutual references between these two files.

from src import routes
from src.database import models, initdb
