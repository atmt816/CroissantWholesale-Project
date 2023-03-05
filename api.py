import mysql.connector
from mysql.connector import Error
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


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name

        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occured.")
    return connection


# setting up the application
app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = True  # allow to show error in browser


app.run()
