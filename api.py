import mysql.connector
from mysql.connector import Error
import hashlib
import datetime
import time
import flask  # , werkzeug
from flask import request, jsonify
import datetime
import time 
from flask import jsonify
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

# function that will be called in the main file to carry out the query in the app.route in which it is used in


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}'")

# i am planning to use this function with the app routes that pertain to the logs table


def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# setting up the application
app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = True  # allow to show error in browser


#---- EMPLOYEE PAGE ----- 

# employees get method working now
# not returning data for now since roles table is empty
# adjust sql as needed - Misael
@app.route('/employees', methods=['GET'])
def employee_info():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    # sql = "SELECT * FROM employees"
    sql = """
        SELECT e.emp_id, e.first_name, e.last_name, e.start_date, e.end_date, e.emp_status, r.role_name
        FROM employees AS e
        JOIN roles AS r
        ON e.role_id = r.role_id;
        """
    employees = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM states;
        """ 
    states = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM roles;
        """ 
    roles = execute_read_query(conn, sql)

    return jsonify(employees, states, roles)


# employee_contact get method working now
# adjust sql as needed - Misael
@app.route('/emp_info', methods=['GET'])
def get_employee_contact():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """SELECT e.emp_id, e.first_name, e.last_name, e.start_date, e.end_date, e.emp_status, r.role_name, ec.phone, ec.email, ec.street, ec.city, s.state_code_id, ec.zipcode
            FROM employees e
            JOIN employee_contact ec
            ON e.emp_id = ec.emp_id
            JOIN roles AS r
			ON e.role_id = r.role_id
            JOIN states s
            ON ec.state_code_id = s.state_code_id;"""
    employee_info = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM states;
        """ 
    states = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM roles;
        """ 
    roles = execute_read_query(conn, sql)

    # sql = """SELECT * FROM states"""
    return jsonify(employee_info, states, roles)



@app.route('/employees/add', methods = ['POST'])
def add_employee():
    conn = create_connection(
    'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    request_data = request.get_json()
    first_name = request_data['first_name']
    last_name= request_data['last_name']  
    start_date = request_data['start_date']
    end_date = request_data['end_date']
    emp_status = request_data['emp_status']
    role_id = request_data['role_id']     
    phone = request_data['phone']    
    email = request_data['email']
    street = request_data['street']
    city = request_data['city']   
    state_code_id = request_data['state_code_id']     
    zipcode = request_data['zipcode']  
    
    sql = """
    INSERT INTO employees (first_name, last_name, start_date, end_date, emp_status, role_id) 
    VALUES ('%s', '%s', '%s', '%s', '%s', %s);
    """ %(first_name, last_name, start_date, end_date, emp_status, role_id)
    execute_query(conn, sql)
    # gets the customer id from the above execution
    sql = 'SELECT * FROM employees WHERE emp_id= LAST_INSERT_ID()' 
    emp_id = execute_read_query(conn, sql)
    emp_id = emp_id[0]['emp_id']
    # Stores Customer Contacts Information 
    sql = """
    INSERT INTO customer_contacts (emp_id, phone, email, street, city, state_code_id, zipcode) 
    VALUES (%s, %s, '%s', '%s','%s', '%s', %s)
    """%(emp_id, phone, email, street, city, state_code_id, zipcode)
    execute_query(conn, sql)
    return "Employee has been added"





# customers get method working now
# no data in customers for now
# adjust sql as needed - Misael
@app.route('/customers', methods=['GET'])
def get_customers():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM customers"
    customers = execute_read_query(conn, sql)
    return jsonify(customers)


# inventory get method working now
# no data in inventory for now
# adjust sql as needed - Misael
@app.route('/inventory', methods=['GET'])
def get_inventory():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM inventory"
    inventory = execute_read_query(conn, sql)
    return inventory


# invoices get method working now
# no data in invoices for now
# adjust sql as needed - Misael
@app.route('/invoices', methods=['GET'])
def get_invoices():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM inventory"
    invoices = execute_read_query(conn, sql)
    return invoices


# maintenance get method working now
# adjust sql as needed - Misael
@app.route('/maintenance', methods=['GET'])
def get_maintenance():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM maintenance_logs"
    maintenance = execute_read_query(conn, sql)
    return maintenance


app.run()
