import hashlib
import datetime
import time
import flask  # , werkzeug
from flask import jsonify, make_response
from flask import request, make_response
# from sql import create_connection
# from sql import execute_read_query
# from sql import execute_query
from datetime import datetime

# setting up the application
app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = True  # allow to show error in browser


app.run()
