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


# ---- EMPLOYEE PAGE -----

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



@app.route('/employees/<emp_id>', methods=['GET'])
def get_employee_info(emp_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """
        SELECT e.emp_id, e.first_name, e.last_name, e.start_date, e.end_date, e.emp_status, r.role_name, ec.phone, ec.email, ec.street, ec.city, s.state_code_id, ec.zipcode
            FROM employees e
            JOIN employee_contact ec
            ON e.emp_id = ec.emp_id
            JOIN roles AS r
			ON e.role_id = r.role_id
            JOIN states s
            ON ec.state_code_id = s.state_code_id
        WHERE e.emp_id = '%s';
        """ % (emp_id)

    employees = execute_read_query(conn, sql)
    # print(sql)
    sql = """
         SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)

    sql = """ SELECT * FROM roles;"""
    roles = execute_read_query(conn, sql)

    return jsonify(employees, states, roles)


@app.route('/employees/add', methods=['POST'])
def add_employee():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    request_data = request.get_json()

    first_name = request_data['first_name']
    last_name = request_data['last_name']
    start_date = request_data['start_date']
    emp_status = request_data['emp_status']
    role_id = request_data['role_id']
    phone = request_data['phone']
    email = request_data['email']
    street = request_data['street']
    city = request_data['city']
    state_code_id = request_data['state_code_id']
    zipcode = request_data['zipcode']

    sql = """
    INSERT INTO employees (first_name, last_name, start_date, emp_status, role_id) 
    VALUES ('%s', '%s', '%s', '%s', %s);
    """ % (first_name, last_name, start_date, emp_status, role_id)
    execute_query(conn, sql)
    # gets the customer id from the above execution
    sql = 'SELECT * FROM employees WHERE emp_id= LAST_INSERT_ID()'
    emp_id = execute_read_query(conn, sql)
    emp_id = emp_id[0]['emp_id']
    # Stores Customer Contacts Information
    sql = """
    INSERT INTO employee_contact (emp_id, phone, email, street, city, state_code_id, zipcode) 
    VALUES (%s, %s, '%s', '%s','%s', '%s', %s)
    """ % (emp_id, phone, email, street, city, state_code_id, zipcode)
    execute_query(conn, sql)
    return "Employee has been added"


@app.route('/update_employee/', methods=['PUT'])
def update_employee():
    # The user input is gathered in JSON format and stored into an empty variable
    update_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    emp_id = update_data['emp_id']
    first_name = update_data['first_name']
    last_name = update_data['last_name']
    start_date = update_data['start_date']
    end_date = update_data['end_date']
    emp_status = update_data['emp_status']
    role_id = update_data['role_id']
    phone = update_data['phone']
    email = update_data['email']
    street = update_data['street']
    city = update_data['city']
    state_code_id = update_data['state_code_id']
    zipcode = update_data['zipcode']

    # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    # fmt_start_date = str(datetime.strptime(start_date, '%m-%d-%Y').date())

    # fmt_end_date = "null"
    # if end_date != "null" and end_date != "NULL":
    #     fmt_end_date = str(datetime.strptime(end_date, '%m-%d-%Y').date())

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    # update employees table
    cursor = conn.cursor()
    sql = "UPDATE employees SET first_name = %s, last_name = %s, start_date = %s, end_date = %s, emp_status = %s, role_id = %s WHERE emp_id = %s"
    val = (first_name, last_name,
           start_date, end_date, emp_status, role_id, emp_id)
    cursor.execute(sql, val)

    # update employee contacts table
    sql = "UPDATE employee_contact SET phone = %s, email = %s, street = %s, city = %s, state_code_id = %s, zipcode = %s WHERE emp_id = %s"
    val = (phone, email, street, city, state_code_id, zipcode, emp_id)
    cursor.execute(sql, val)

    conn.commit()
    return 'Employee was updated successfully'




############################# ROLES PAGE #######################################

# Roles Table CRUD


@app.route('/roles', methods=['GET'])
def get_roles():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM roles"
    roles = execute_read_query(conn, sql)
    return jsonify(roles)

# sql script used to create roles table is missing auto_increment for Role_ID********
# either have to redo table or add in Role_ID to the insert below ******


@app.route('/addrole', methods=['POST'])
def add_role():
    # The user input is gathered in JSON format and stored into an empty variable
    role_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    role_name = role_data['role_name']
    role_description = role_data['role_description']
    role_status = role_data['role_status']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO roles(role_name, role_description, role_status) VALUES ('%s', '%s', '%s')" % (
        role_name, role_description, role_status)

    execute_query(conn, sql)
    return 'Role was added Successfully'


@app.route('/roles/<role_id>', methods=['GET'])
def get_roles_info(role_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """
        SELECT * FROM cid4375.roles where role_id = '%s';
        """ % (role_id)

    roles = execute_read_query(conn, sql)

    return jsonify(roles)

# PUT method for roles


@app.route('/update_role', methods=['PUT'])
def update_role():
    # The user input is gathered in JSON format and stored into an empty variable
    role_data = request.get_json()
    # we will be using Role_ID to reference the entry to update
    role_id = role_data['role_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    role_name = role_data['role_name']
    role_description = role_data['role_description']
    role_status = role_data['role_status']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE roles SET role_name = %s, role_description = %s, role_status = %s WHERE role_id = %s"
    val = (role_name, role_description, role_status, role_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Role was updated successfully'


##################################### CUSTOMERS ###################################

# Customers Table CRUD

# customers get method working now
# no data in customers for now
# adjust sql as needed - Misael


@app.route('/customers', methods=['GET'])
def get_customers():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM customers"
    customers = execute_read_query(conn, sql)

    sql = """
         SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)

    return jsonify(customers, states)


@app.route('/customers/<customer_id>', methods=['GET'])
def get_customer_info(customer_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """SELECT c.customer_id, c.business_name, c.first_name, c.last_name, c.cust_acc_num, c.business_hrs, c.customer_status, cc.phone, cc.email, cc.street, cc.city, cc.zipcode, cc.state_code_id
        FROM customers c
        JOIN customer_contact cc ON c.customer_id = cc.customer_id
        JOIN states s ON cc.state_code_id = s.state_code_id
        WHERE c.customer_id = '%s';
        """ % (customer_id)
    customers = execute_read_query(conn, sql)

    sql = """
         SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)

    return jsonify(customers, states)


# Customers Insert Method
@app.route('/customers/add', methods=['POST'])
def add_customer():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    # The user input is gathered in JSON format and stored into an empty variable
    request_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    business_name = request_data['business_name']
    business_hrs = request_data['business_hrs']
    last_name = request_data['last_name']
    first_name = request_data['first_name']
    cust_acc_num = request_data['cust_acc_num']
    customer_status = request_data['customer_status']
    phone = request_data['phone']
    email = request_data['email']
    street = request_data['street']
    city = request_data['city']
    state_code_id = request_data['state_code_id']
    zipcode = request_data['zipcode']

    sql = """
    INSERT INTO customers (business_name, business_hrs, last_name, first_name, cust_acc_num, customer_status) VALUES ('%s', '%s', '%s', '%s', %s, '%s')
    """ % (business_name, business_hrs, last_name, first_name, cust_acc_num, customer_status)

    execute_query(conn, sql)

    # gets the customer id from the above execution
    sql = 'SELECT * FROM customers WHERE customer_id= LAST_INSERT_ID()'
    customer_id = execute_read_query(conn, sql)
    customer_id = customer_id[0]['customer_id']
    # customer_id = request_data['customer_id']

    sql = """INSERT INTO customer_contact(customer_id, phone, email, street, city, state_code_id, zipcode ) VALUES (%s, %s, '%s', '%s', '%s', '%s', %s)""" % (
        customer_id, phone, email, street, city, state_code_id, zipcode)

    execute_query(conn, sql)

    return 'Customer was added Successfully'

# Customers Update Method


@app.route('/update_customer/', methods=['PUT'])
def update_customer():
    # The user input is gathered in JSON format and stored into an empty variable
    customer_data = request.get_json()
    # we will be using customer_id to reference the entry to update
    customer_id = customer_data['customer_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    business_name = customer_data['business_name']
    business_hrs = customer_data['business_hrs']
    last_name = customer_data['last_name']
    first_name = customer_data['first_name']
    cust_acc_num = customer_data['cust_acc_num']
    customer_status = customer_data['customer_status']
    phone = customer_data['phone']
    email = customer_data['email']
    street = customer_data['street']
    city = customer_data['city']
    state = customer_data['state_code_id']
    zipcode = customer_data['zipcode']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    # Update customers table
    cursor = conn.cursor()
    sql = "UPDATE customers SET business_name = %s, business_hrs = %s, last_name = %s, first_name = %s, cust_acc_num = %s, customer_status = %s WHERE customer_id = %s"
    val = (business_name, business_hrs, last_name,
           first_name, cust_acc_num, customer_status, customer_id)
    cursor.execute(sql, val)

    # Update customer contacts table
    cursor = conn.cursor()
    sql = "UPDATE customer_contact SET Phone = %s, Email = %s, Street = %s, City = %s, state_code_id = %s, zipcode = %s WHERE customer_id = %s"
    val = (phone, email, street, city, state, zipcode, customer_id)

    cursor.execute(sql, val)

    conn.commit()
    return 'Customer was updated successfully'


# ---- Vendors PAGE -----

# vendors get method working now - Misael
@app.route('/vendors', methods=['GET'])
def vendors():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    # sql = "SELECT * FROM employees"
    sql = """
        SELECT v.vendor_id, v.vendor_name, v.vendor_hrs, v.vendor_account_number, v.vendor_status, vc.phone, vc.email, vc.street, vc.city, vc.zipcode, s.state_code_id 
        FROM vendors v JOIN vendor_contacts vc ON v.vendor_id = vc.vendor_id
        JOIN states s ON vc.state_code_id = s.state_code_id
        """
    vendors = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)

    return jsonify(vendors, states)

# vendor info get method by id working now - Misael


@app.route('/vendors/<vendor_id>', methods=['GET'])
def vendor_info(vendor_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    sql = """
        SELECT v.vendor_id, v.vendor_name, v.vendor_hrs, v.vendor_account_number, v.vendor_status, vc.phone, vc.email, vc.street, vc.city, vc.zipcode, s.state_code_id 
        FROM vendors v JOIN vendor_contacts vc ON v.vendor_id = vc.vendor_id
        JOIN states s ON vc.state_code_id = s.state_code_id
        WHERE v.vendor_id = '%s';
        """ % (vendor_id)
    vendor = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)

    return jsonify(vendor, states)


@app.route('/vendors/add', methods=['POST'])
def add_vendor():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    request_data = request.get_json()

    vendor_name = request_data['vendor_name']
    vendor_hrs = request_data['vendor_hrs']
    vendor_account_number = request_data['vendor_account_number']
    vendor_status = request_data['vendor_status']
    phone = request_data['phone']
    email = request_data['email']
    street = request_data['street']
    city = request_data['city']
    state_code_id = request_data['state_code_id']
    zipcode = request_data['zipcode']

    sql = """
    INSERT INTO vendors (vendor_name, vendor_hrs, vendor_account_number, vendor_status) 
    VALUES ('%s', '%s', %s, '%s');
    """ % (vendor_name, vendor_hrs, vendor_account_number, vendor_status)
    execute_query(conn, sql)
    # gets the customer id from the above execution
    sql = 'SELECT * FROM vendors WHERE vendor_id = LAST_INSERT_ID()'
    vendor_id = execute_read_query(conn, sql)
    vendor_id = vendor_id[0]['vendor_id']
    # Stores Customer Contacts Information

    sql = """
    INSERT INTO vendor_contacts (vendor_id, phone, email, street, city, state_code_id, zipcode) 
    VALUES (%s, %s, '%s', '%s', '%s','%s', %s)
    """ % (vendor_id, phone, email, street, city, state_code_id, zipcode)
    execute_query(conn, sql)
    return "Vendor has been added"


@app.route('/update_vendor/', methods=['PUT'])
def update_vendor():
    # The user input is gathered in JSON format and stored into an empty variable
    vendor_data = request.get_json()
    # we will be using customer_id to reference the entry to update
    vendor_id = vendor_data['vendor_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    vendor_name = vendor_data['vendor_name']
    vendor_hrs = vendor_data['vendor_hrs']
    vendor_account_number = vendor_data['vendor_account_number']
    vendor_status = vendor_data['vendor_status']
    phone = vendor_data['phone']
    email = vendor_data['email']
    street = vendor_data['street']
    city = vendor_data['city']
    state_code_id = vendor_data['state_code_id']
    zipcode = vendor_data['zipcode']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    # Update vendor table
    cursor = conn.cursor()
    sql = "UPDATE vendors SET vendor_name = %s, vendor_hrs = %s, vendor_account_number = %s, vendor_status = %s WHERE vendor_id = %s"
    val = (vendor_name, vendor_hrs, vendor_account_number,
           vendor_status, vendor_id)
    cursor.execute(sql, val)

    # Update customer contacts table
    cursor = conn.cursor()
    sql = "UPDATE vendor_contacts SET Phone = %s, Email = %s, Street = %s, City = %s, state_code_id = %s, zipcode = %s WHERE vendor_id = %s"
    val = (phone, email, street, city, state_code_id, zipcode, vendor_id)

    cursor.execute(sql, val)

    conn.commit()
    return 'Customer was updated successfully'


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




# # maintenance get method working now
# # adjust sql as needed - Misael
# @app.route('/maintenance', methods=['GET'])
# def get_maintenance():
#     conn = create_connection(
#         'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
#     sql = "SELECT * FROM maintenance_logs"
#     maintenance = execute_read_query(conn, sql)
#     return maintenance


#GARAGE PAGE

@app.route('/garage', methods=['GET'])
def get_garage():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM garage"
    garage = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)


    return jsonify(garage, states)

#Specifc garage id get for modal info
@app.route('/garage/<garage_id>', methods=['GET'])
def get_garage_info(garage_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM garage WHERE garage_id = %s" % (garage_id)
    garage = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)


    return jsonify(garage, states)


@app.route('/addgarage', methods=['POST'])
def add_garage():
    # The user input is gathered in JSON format and stored into an empty variable
    garage_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    garage_name = garage_data['garage_name']
    garage_hrs = garage_data['garage_hrs']
    phone = garage_data['phone']
    street = garage_data['street']
    city = garage_data['city']
    state_code_id = garage_data['state_code_id']
    zipcode = garage_data['zipcode']
    status = garage_data['status']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO garage(garage_name, phone, street, city, state_code_id, zipcode, status, garage_hrs) VALUES ('%s', %s, '%s', '%s', '%s', %s, '%s', '%s')" % (
        garage_name, phone, street, city, state_code_id, zipcode, status, garage_hrs)

    execute_query(conn, sql)
    return 'Garage was added Successfully'


# PUT method for garage
@app.route('/update_garage', methods=['PUT'])
def update_garage():
    # The user input is gathered in JSON format and stored into an empty variable
    garage_data = request.get_json()
    # we will be using garage_id to reference the entry to update
    garage_id = garage_data['garage_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    garage_name = garage_data['garage_name']
    phone = garage_data['phone']
    street = garage_data['street']
    city = garage_data['city']
    state= garage_data['state_code_id']
    zipcode = garage_data['zipcode']
    status = garage_data['status']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE garage SET garage_name = %s, phone = %s, street = %s, city = %s, state_code_id = %s, zipcode = %s, status = %s WHERE garage_id = %s"
    val = (garage_name, phone, street, city, state, zipcode ,status , garage_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Garage was updated successfully'

############################# VEHICLES ###################################


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM vehicles"
    vehicles = execute_read_query(conn, sql)
    return jsonify(vehicles)

@app.route('/addvehicle', methods=['POST'])
def add_vehicle():
    # The user input is gathered in JSON format and stored into an empty variable
    vehicle_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    license_plate = vehicle_data['license_plate']
    make = vehicle_data['make']
    model = vehicle_data['model']
    vin = vehicle_data['vin']
    status = vehicle_data['status']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO vehicles(license_plate, make, model, vin, status) VALUES ('%s', '%s', '%s', '%s', '%s')" % (
        license_plate, make, model, vin, status)

    execute_query(conn, sql)
    return 'Vehicle was added Successfully'

# PUT method for vehicles
@app.route('/update_vehicle', methods=['PUT'])
def update_vehicle():
    # The user input is gathered in JSON format and stored into an empty variable
    vehicle_data = request.get_json()
    # we will be using vehicle_id to reference the entry to update
    vehicle_id = vehicle_data['vehicle_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    license_plate = vehicle_data['license_plate']
    make = vehicle_data['make']
    model = vehicle_data['model']
    vin = vehicle_data['vin']
    status = vehicle_data['status']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE vehicles SET license_plate = %s, make = %s, model = %s, vin = %s,status = %s WHERE vehicle_id = %s"
    val = (license_plate, make, model, vin, status, vehicle_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Vehicle was updated successfully'

# Get specific vehicle info with maintenence log data for modal 
@app.route('/vehicles/<vehicle_id>', methods=['GET'])
def get_vehicles_info(vehicle_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """SELECT * FROM vehicles
        WHERE vehicle_id = '%s';""" % (vehicle_id)
    vehicles = execute_read_query(conn, sql)

    sql = """SELECT v.vehicle_id, ml.log_id, ml.date, ml.status, ml.note, g.garage_name, g.phone, g.garage_hrs
            FROM vehicles v
            JOIN maintenance_logs ml
            ON v.vehicle_id = ml.vehicle_id
            JOIN garage AS g
            ON ml.garage_id = g.garage_id
            JOIN states s
            ON g.state_code_id = s.state_code_id
        WHERE v.vehicle_id = '%s';""" % (vehicle_id)
    maintenance_info = execute_read_query(conn, sql)

    return jsonify(vehicles, maintenance_info)


# Maintenance_Logs Table CRUD


# maintenance get method working now
# adjust sql as needed - Misael
@app.route('/maintenance', methods=['GET'])
def get_maintenance():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    # sql = "SELECT * FROM employees"
    sql = """
        SELECT logs.log_id, v.license_plate, g.garage_name ,logs.date, logs.status, logs.note 
        FROM maintenance_logs AS logs 
        INNER JOIN vehicles AS v ON logs.vehicle_id = v.vehicle_id 
        INNER JOIN garage AS g ON logs.garage_id = g.garage_id 
        ORDER BY date DESC;
        """
    maintenance = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM garage;
        """
    garage = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM vehicles;
        """
    vehicles = execute_read_query(conn, sql)

    return jsonify(maintenance, garage, vehicles)

#Specific maintenance log details for selected row
@app.route('/maintenance/<log_id>', methods=['GET'])
def get_maintenance_info(log_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT logs.log_id, v.license_plate , g.garage_name ,g.phone,g.street,g.city,g.state_code_id,g.zipcode, logs.date , logs.status , logs.note  FROM maintenance_logs AS logs INNER JOIN vehicles AS v ON logs.vehicle_id = v.vehicle_id INNER JOIN garage AS g ON logs.garage_id = g.garage_id WHERE logs.log_id = %s;" % (log_id)
    maintenance = execute_read_query(conn, sql)
    return jsonify(maintenance)

# PUT method for maintenance_logs
@app.route('/update_maintenance_log', methods=['PUT'])
def update_maintenance_log():
    # The user input is gathered in JSON format and stored into an empty variable
    maintenance_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    log_id = maintenance_data['log_id']
    date = maintenance_data['date']
    status = maintenance_data['status']
    note = maintenance_data['note']

    # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    #fmt_date = str(datetime.strptime(date, '%m-%d-%Y').date())

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE maintenance_logs SET date = %s, status = %s, note = %s WHERE log_id = %s"
    val = (date, status, note, log_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Maintenance Log was updated successfully'

@app.route('/deletemaintenance', methods=['PUT'])
def delete_maintenance_info():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    maintenance_data = request.get_json()
    log_id = maintenance_data['log_id']
    sql = "DELETE FROM maintenance_logs WHERE log_id = %s" % (log_id)
    execute_query(conn,sql)
    print(log_id)
    return 'Maintenance log was successfully deleted'

@app.route('/addmaintenancelog', methods=['POST'])
def add_maintenance_log():
    # The user input is gathered in JSON format and stored into an empty variable
    log_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    garage_id = log_data['garage_id']
    vehicle_id = log_data['vehicle_id']
    date = log_data['date']
    status = log_data['status']
    note = log_data['note']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO maintenance_logs(garage_id, vehicle_id, date, status, note) VALUES (%s, %s, '%s', '%s', '%s')" % (
        garage_id, vehicle_id, date, status, note)

    execute_query(conn, sql)
    return 'Maintenance Log was added Successfully'


# Maintenance Log by Vehicle - Generates a report for all maintenance logs under a specified vehicle id.

@app.route('/vehiclemaintenancelog/<vehicle_id>', methods=['GET'])
def get_vehicle_main_log(vehicle_id):
    selected_vehicle_id = request.get_json()
    vehicle_id = selected_vehicle_id['vehicle_id']
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT g.garage_name AS 'Garage Name', logs.date AS 'Date', logs.status AS 'Status', logs.note AS 'note' FROM maintenance_logs AS logs INNER JOIN vehicles AS v ON logs.vehicle_id = v.vehicle_id INNER JOIN garage AS g ON logs.garage_id = g.garage_id WHERE v.vehicle_id = %s ORDER BY date DESC;  " % (
        vehicle_id)
    vehicle_main_log = execute_read_query(conn, sql)
    return jsonify(vehicle_main_log)


# Maintenance Log by Garage - Generates a report for all maintenance logs under a specified garage id.

@app.route('/garagemaintenancelog/<garage_id>', methods=['GET'])
def get_garagemain_log(garage_id):
    selected_garage_id = request.get_json()
    garage_id = selected_garage_id['garage_id']
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT v.license_plate AS 'License Plate', logs.date AS 'Date', logs.status AS 'Status', logs.note AS 'note' FROM maintenance_logs AS logs INNER JOIN vehicles AS v ON logs.vehicle_id = v.vehicle_id INNER JOIN garage AS g ON logs.garage_id = g.garage_id WHERE g.garage_id = %s ORDER BY date DESC" % (
        garage_id)
    garage_main_log = execute_read_query(conn, sql)
    return jsonify(garage_main_log)


############################# INVOICES ######################################

# Invoices Table CRUD

#Return all invoices 
@app.route('/invoices', methods=['GET'])
def get_invoices():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT i.invoice_id, i.customer_id, i.invoice_date, i.invoice_total, i.payment_status, i.date_paid, i.order_id, c.business_name FROM invoices as i INNER JOIN customers as c on i.customer_id = c.customer_id;"
    invoices = execute_read_query(conn, sql)

    return jsonify(invoices)

#Retrieve specific invoice data
@app.route('/invoices/<invoice_id>', methods=['GET'])
def get_invoice_info(invoice_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """
        SELECT * FROM invoices
        WHERE invoice_id = %s;
        """ % (invoice_id)
    
    invoices = execute_read_query(conn, sql)

    sql = """SELECT i.invoice_id, c.business_name, cc.phone, cc.email, cc.street, cc.city, cc.state_code_id, cc.zipcode
            FROM invoices i
            JOIN customers c
            ON i.customer_id = c.customer_id
            JOIN customer_contact AS cc
            ON cc.customer_id = c.customer_id
            JOIN states s
            ON s.state_code_id = cc.state_code_id
        WHERE i.invoice_id = '%s';""" % (invoice_id)
    
    customer_info = execute_read_query(conn, sql)

    sql = """SELECT li.product_id, li.quantity, li.price_per_unit, li.total, p.product_name
            FROM invoices i
            JOIN line_items AS li
            ON i.order_id = li.order_id
            JOIN products p
            ON li.product_id = p.product_id
        WHERE i.invoice_id = '%s';""" % (invoice_id)
    
    order_info = execute_read_query(conn, sql)

    sql = """SELECT o.delivery_date
            FROM orders o
            JOIN invoices AS i
            ON o.order_id = i.order_id
        WHERE i.invoice_id = '%s';""" % (invoice_id)
    delivery_date = execute_read_query(conn, sql)

    return jsonify(invoices, customer_info, order_info, delivery_date)

# PUT method for invoices
@app.route('/update_invoices', methods=['PUT'])
def update_invoices():
    # The user input is gathered in JSON format and stored into an empty variable
    invoice_data = request.get_json()
    # we will be using invoice_id to reference the entry to update
    invoice_id = invoice_data['invoice_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    customer_id = invoice_data['customer_id']
    invoice_date = invoice_data['invoice_date']
    invoice_total = invoice_data['invoice_total']
    payment_status = invoice_data['payment_status']
    date_paid = invoice_data['date_paid']

    # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    fmt_invoice_date = str(datetime.strptime(
        invoice_date, '%m-%d-%Y').date())
    # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    fmt_date_paid = str(datetime.strptime(
        date_paid, '%m-%d-%Y').date())

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE invoices SET vendor_id = %s, customer_id = %s, invoice_number = %s, invoice_date = %s, invoice_total = %s, payment_status = %s, date_paid = %s WHERE invoice_id = %s"
    val = (customer_id, fmt_invoice_date,
           invoice_total, payment_status, fmt_date_paid, invoice_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Invoice was updated successfully'


############################# PRODUCTS ###################################

# Products Table CRUD

@app.route('/products', methods=['GET'])
def get_products():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM products"
    products = execute_read_query(conn, sql)
    return jsonify(products)

@app.route('/products/<product_id>', methods=['GET'])
def get_product_info(product_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """
        SELECT * FROM products
        WHERE product_id = %s;
        """ % (product_id)

    product = execute_read_query(conn, sql)
    return jsonify(product)


@app.route('/add_product', methods=['POST'])
def add_product():
    # The user input is gathered in JSON format and stored into an empty variable
    product_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    product_name = product_data['product_name']
    product_status = product_data['product_status']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO products(product_name, product_status) VALUES ('%s', '%s')" % (
        product_name, product_status)

    execute_query(conn, sql)
    return 'Product was added Successfully'

@app.route('/update_product', methods=['PUT'])
def update_product():
    # The user input is gathered in JSON format and stored into an empty variable
    product_data = request.get_json()
    
    product_id = product_data['product_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    product_name = product_data['product_name']
    product_status = product_data['product_status']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE products SET product_name = %s, product_status = %s WHERE product_id = %s"
    val = (product_name, product_status, product_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Product was updated successfully'


#*********** ORDERS PAGE ****************************

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    # sql = "SELECT * FROM orders;"
    sql = """
    SELECT o.date_produced, o.delivery_date, o.status, c.business_name, o.customer_id, o.order_id from customers as c join orders as o on c.customer_id =o.customer_id;
    """
    orders = execute_read_query(conn, sql)

    sql = """
         SELECT * FROM customers;
        """
    customers = execute_read_query(conn, sql)

    # sql= """
    #     SELECT c.business_name, o.customer_id from customers as c join orders as o on c.customer_id =o.customer_id;
    #     """
    # customer_name = execute_read_query(conn, sql)

    sql = """
         SELECT * FROM products;
        """
    products = execute_read_query(conn, sql)

    sql = """
         SELECT * FROM line_items;
        """
    line_items = execute_read_query(conn, sql)

    return jsonify(orders, customers, products, line_items)


@app.route('/addorder', methods=['POST'])
def add_order():
    # The user input is gathered in JSON format and stored into an empty variable
    order_data = request.get_json()
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    # The JSON object is then separated into variables so that they may be used in a sql query
    sql = """
         SELECT CURDATE();
        """
    date_produced = execute_read_query(conn, sql)

    customer_id = order_data['customer_id']
    status = order_data['status']
    line_items = order_data['line_items']
    current_date = date_produced[0]['CURDATE()']

    sql = "INSERT INTO orders(date_produced, status, customer_id) VALUES ('%s', '%s', %s)" % (
        current_date, status, customer_id)
    execute_query(conn, sql)

    # gets the order id from the above execution
    sql = 'SELECT * FROM orders WHERE order_id= LAST_INSERT_ID()'
    order_id = execute_read_query(conn, sql)
    order_id = order_id[0]['order_id']

    # Set up future invoice with corresponding ids
    sql = "INSERT INTO invoices(customer_id, order_id) VALUES (%s, %s)" % (
        customer_id, order_id)
    execute_query(conn, sql)

    sql = "INSERT INTO line_items (order_id, product_id, quantity, price_per_unit, total) VALUES"

    list_length = len(line_items)-1
    index = 0
    for item in line_items:
        product_id = item['product_id']
        quantity = item['quantity']
        price_per_unit = item['price_per_unit']
        total = item['total']
        sql += " (%s, %s, %s, %s, %s)" % (order_id,
                                          product_id, quantity, price_per_unit, total)
        if index < list_length:
            sql += ", "
            index = index + 1

    execute_query(conn, sql)

    return 'Order was added Successfully'


@app.route('/orders/<order_id>', methods=['GET'])
def order_info(order_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    # order information
    sql = """
        SELECT o.order_id, o.date_produced, o.delivery_date, o.status, o.customer_id, l.product_id, p.product_name, l.quantity, l.price_per_unit, l.total
        FROM orders o 
        JOIN line_items l ON o.order_id = l.order_id
        JOIN products p ON l.product_id = p.product_id
        WHERE o.order_id ='%s';
        """ % (order_id)
    order = execute_read_query(conn, sql)

    customer_id = order[0]['customer_id']

    sql = """
        select c.customer_id, c.business_name, cc.phone, cc.email, cc.street, cc.city, cc.state_code_id, cc.zipcode
        FROM customers c JOIN customer_contact cc 
        ON c.customer_id = cc.customer_id 
        WHERE c.customer_id ='%s';
        """ % (customer_id)
    customer = execute_read_query(conn, sql)

    sql = """
        SELECT * FROM products;
        """
    products = execute_read_query(conn, sql)

    sql = """SELECT * FROM customers;"""
    customers_data = execute_read_query(conn, sql)

    sql = """SELECT sum(total) FROM line_items WHERE order_id ='%s';""" % (
        order_id)
    total = execute_read_query(conn, sql)

    return jsonify(order, customer, products, customers_data, total)


@app.route('/update_order', methods=['PUT'])
def update_order():
    # The user input is gathered in JSON format and stored into an empty variable
    order_data = request.get_json()
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    order_id = order_data['order_id']
    customer_id = order_data['customer_id']
    status = order_data['status']
    delivery_date = order_data['delivery_date']
    line_items = order_data['line_items']

    sql = "UPDATE orders SET customer_id= %s, delivery_date= '%s', status= '%s' WHERE order_id= %s" % (
        customer_id, delivery_date, status, order_id)
    execute_query(conn, sql)

    sql = "DELETE FROM line_items WHERE order_id= %s" % (order_id)
    execute_query(conn, sql)

    sql = "INSERT INTO line_items (order_id, product_id, quantity, price_per_unit, total) VALUES"

    list_length = len(line_items)-1
    index = 0
    for item in line_items:

        product_id = item['product_id']
        quantity = item['quantity']
        price_per_unit = item['price_per_unit']
        total = item['total']
        sql += " (%s, %s, %s, %s, %s)" % (order_id,
                                          product_id, quantity, price_per_unit, total)
        if index < list_length:
            sql += ", "
            index = index + 1

    execute_query(conn, sql)

    return 'Order was updated Successfully'


@app.route('/orders_delete', methods=['DELETE'])
def delete_order():
    order_data = request.get_json()
    order_id = order_data['order_id']
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    cursor = conn.cursor()
    # sql = "SELECT * FROM orders;"
    sql = "DELETE FROM line_items WHERE order_id= %s"
    val = (order_id)

    sql = "DELETE FROM invoices WHERE order_id= %s"
    val = (order_id)

    sql = "DELETE FROM orders WHERE order_id= %s"
    val = (order_id)
    
    cursor.execute(sql, val)
    conn.commit
    return 'Order was deleted successfully'

# Best Selling Items Report
# This report generates a count for each specific line item's frequency across all orders.

# Daily Best Sellers - Determine most popular items amongst all orders scheduled for delivery on current date.
@app.route('/dailybestsellers', methods=['GET'])
def get_daily_best_sell_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit, O.Order_ID, LI.Quantity, COUNT(O.Order_ID) AS Order_Frequency FROM orders AS O INNER JOIN line_items AS LI ON LI.Order_ID = O.Order_ID INNER JOIN products as P ON P.Product_ID = LI.Product_ID WHERE O.Delivery_Date = curdate() GROUP BY P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit"
    daily_best_sell_report = execute_read_query(conn, sql)
    return jsonify(daily_best_sell_report)


# # Orders Table CRUD

    
# Weekly Best Sellers - Determine most popular items amongst all orders scheduled for delivery within a week from the current date.


# @app.route('/weeklybestsellers', methods=['GET'])
# def get_weekly_best_sell_report():
#     conn = create_connection(
#         'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
#     sql = "SELECT P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit, O.Order_ID, LI.Quantity, COUNT(O.Order_ID) AS Order_Frequency FROM orders AS O INNER JOIN line_items AS LI ON LI.Order_ID = O.Order_ID INNER JOIN products as P ON P.Product_ID = LI.Product_ID WHERE O.Delivery_Date BETWEEN curdate() AND curdate()+8 GROUP BY P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit"
#     weekly_best_sell_report = execute_read_query(conn, sql)
#     return jsonify(weekly_best_sell_report)

# # Monthly Best Sellers - Determine most popular items amongst all orders scheduled for delivery within a month from the current date.


# @app.route('/monthlybestsellers', methods=['GET'])
# def get_monthly_best_sell_report():
#     conn = create_connection(
#         'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
#     sql = "SELECT P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit, O.Order_ID, LI.Quantity, COUNT(O.Order_ID) AS Order_Frequency FROM orders AS O INNER JOIN line_items AS LI ON LI.Order_ID = O.Order_ID INNER JOIN products as P ON P.Product_ID = LI.Product_ID WHERE O.Delivery_Date BETWEEN curdate() AND curdate()+30 GROUP BY P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit"
#     monthly_best_sell_report = execute_read_query(conn, sql)
#     return jsonify(monthly_best_sell_report)

# # Lifetime Best Sellers - Determine most popular items amongst all historical orders.


# @app.route('/lifetimebestsellers', methods=['GET'])
# def get_lifetime_best_sell_report():
#     conn = create_connection(
#         'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
#     sql = "SELECT P.Product_ID, P.Product_Name, COUNT(LI.product_id) AS Order_Frequency FROM orders AS O INNER JOIN line_items AS LI ON LI.Order_ID = O.Order_ID INNER JOIN products as P ON P.Product_ID = LI.Product_ID GROUP BY LI.product_id;"
#     lifetime_best_sell_report = execute_read_query(conn, sql)
#     return jsonify(lifetime_best_sell_report)


@app.route('/vendorinventoryreport', methods=['GET'])
def get_vendor_inv_sheet():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT v.vendor_id, ii.inventory_id, v.vendor_name, ii.item_name, ii.item_amount, ii.unit_cost, ii.total_inv_cost, ii.date_bought FROM vendors AS v JOIN inventory AS ii ON v.vendor_id = ii.vendor_id order by ii.date_bought desc limit 5;"
    vendor_inv_sheet = execute_read_query(conn, sql)
    return jsonify(vendor_inv_sheet)

@app.route('/monthlyordercount', methods=['GET'])
def get_monthly_countt():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT DATE_FORMAT(date_produced, '%M') AS date_produced,COUNT(order_id) AS count FROM orders where Year(date_produced) = year(current_date()) GROUP BY MONTH(date_produced);"
    order_count = execute_read_query(conn, sql)
    return jsonify(order_count)

@app.route('/productcounter', methods=['GET'])
def get_count_product():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "select i.product_id,p.product_name,sum(i.quantity) as total_quantity from line_items as i join products as p on i.product_id = p.product_id join orders as o on i.order_id =o.order_id where o.status='Delivered' group by i.product_id;"
    prod_count = execute_read_query(conn, sql)
    return jsonify(prod_count)

@app.route('/weeklyfulfillmentreport', methods=['GET'])
def get_weekly_ful_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT O.Order_ID, O.Date_Produced, O.Delivery_Date, P.Product_ID, Product_Name, LI.Quantity FROM products AS P INNER JOIN line_items AS LI ON P.Product_ID = LI.Product_ID INNER JOIN orders as O ON O.Order_ID = LI.Order_ID WHERE O.Delivery_Date BETWEEN curdate() AND curdate()+8 GROUP BY O.Order_ID, O.Date_Produced, O.Delivery_Date"
    weekly_ful_report = execute_read_query(conn, sql)
    return jsonify(weekly_ful_report)
app.run()
