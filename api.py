import mysql.connector
from mysql.connector import Error
import hashlib
import datetime
import time
import flask  # , werkzeug
from flask import request, jsonify
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
        return jsonify(result)
    except Error as e:
        print(f"The error '{e}' occured")


# setting up the application
app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = True  # allow to show error in browser


############################# STATES ###################################

# States Table CRUD

@app.route('/states', methods=['GET'])
def get_states():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM states"
    states = execute_read_query(conn, sql)
    return states

############################# EMPLOYEES ###################################

# Employees Table CRUD

# employees get method working now
# not returning data for now since roles table is empty
# adjust sql as needed - Misael

# GET method for employees


@app.route('/employees', methods=['GET'])
def employee_info():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """
        SELECT e.emp_id, e.first_name, e.last_name, e.start_date, e.end_date, e.emp_status, r.role_name
        FROM employees AS e
        JOIN roles AS r
        ON e.role_id = r.role_id;
        """
    employees = execute_read_query(conn, sql)
    return employees

# POST method for employees


@app.route('/addemployee', methods=['POST'])
def add_employee():
    # The user input is gathered in JSON format and stored into an empty variable
    employee_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    first_name = employee_data['first_name']
    last_name = employee_data['last_name']
    start_date = employee_data['start_date']
    end_date = employee_data['end_date']
    emp_status = employee_data['emp_status']
    role_id = employee_data['role_id']

 # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    fmt_start_date = str(datetime.strptime(start_date, '%m-%d-%Y').date())

    fmt_end_date = "null"
    if end_date != "null" and end_date != "NULL":
        fmt_end_date = str(datetime.strptime(end_date, '%m-%d-%Y').date())

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO employees(first_name, last_name, start_date, end_date, emp_status, role_id) VALUES ('%s', '%s', '%s', '%s', '%s', %s)" % (
        first_name, last_name, fmt_start_date, fmt_end_date, emp_status, role_id)

    execute_query(conn, sql)
    return 'Employee was added Successfully'


# PUT method for employees
@app.route('/update_employee', methods=['PUT'])
def update_employee():
    # The user input is gathered in JSON format and stored into an empty variable
    employee_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    emp_id = employee_data['emp_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    first_name = employee_data['first_name']
    last_name = employee_data['last_name']
    start_date = employee_data['start_date']
    end_date = employee_data['end_date']
    emp_status = employee_data['emp_status']
    role_id = employee_data['role_id']

 # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    fmt_start_date = str(datetime.strptime(start_date, '%m-%d-%Y').date())

    fmt_end_date = "null"
    if end_date != "null" and end_date != "NULL":
        fmt_end_date = str(datetime.strptime(end_date, '%m-%d-%Y').date())

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE employees SET first_name = %s, last_name = %s, start_date = %s, end_date = %s, emp_status = %s, role_id = %s WHERE emp_id = %s"
    val = (first_name, last_name,
           fmt_start_date, fmt_end_date, emp_status, role_id, emp_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Employee was updated successfully'

############################# EMPLOYEES CONTACT ###################################

# Employee Contact CRUD

# employee_contact get method working now
# adjust sql as needed - Misael


@app.route('/employee_contact', methods=['GET'])
def get_employee_contact():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """SELECT e.first_name, e.last_name, ec.phone, ec.email, ec.street, ec.city, s.state_code_id, ec.zipcode
           FROM employees e
           JOIN employee_contact ec
            ON e.emp_id = ec.emp_id
            JOIN states s
            ON ec.state_code_id = s.state_code_id;"""
    employee_contact = execute_read_query(conn, sql)

    sql = """SELECT * FROM states"""

    return employee_contact


@app.route('/addemployeecontact', methods=['POST'])
def add_employee_contact():
    # The user input is gathered in JSON format and stored into an empty variable
    employee_contact_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    phone = employee_contact_data['phone']
    email = employee_contact_data['email']
    street = employee_contact_data['street']
    city = employee_contact_data['city']
    state = employee_contact_data['state_code_id']
    zipcode = employee_contact_data['zipcode']
    emp_id = employee_contact_data['emp_id']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO employee_contact(phone, email, street, city, state_code_id, zipcode, emp_id ) VALUES (%s, '%s', '%s', '%s', '%s', %s, %s)" % (
        phone, email, street, city, state, zipcode, emp_id)

    execute_query(conn, sql)
    return 'Employee Contact was added Successfully'


# PUT method for employees_contact
@app.route('/update_employee_contact', methods=['PUT'])
def update_employee_contact():
    # The user input is gathered in JSON format and stored into an empty variable
    employee_contact_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    emp_id = employee_contact_data['emp_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    phone = employee_contact_data['phone']
    email = employee_contact_data['email']
    street = employee_contact_data['street']
    city = employee_contact_data['city']
    state_code_id = employee_contact_data['state_code_id']
    zipcode = employee_contact_data['zipcode']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE employee_contact SET phone = %s, email = %s, street = %s, city = %s, state_code_id = %s, zipcode = %s WHERE emp_id = %s"
    val = (phone, email, street, city, state_code_id, zipcode, emp_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Employee Contact was updated successfully'


############################# ROLES #######################################

# Roles Table CRUD


@app.route('/roles', methods=['GET'])
def get_roles():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM roles"
    roles = execute_read_query(conn, sql)
    return roles

# sql script used to create roles table is missing auto_increment for Role_ID********
# either have to redo table or add in Role_ID to the insert below ******


@app.route('/addrole', methods=['POST'])
def add_role():
    # The user input is gathered in JSON format and stored into an empty variable
    role_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    role_name = role_data['Role_Name']
    role_description = role_data['Role_Description']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO roles(role_name, role_description) VALUES ('%s', '%s')" % (
        role_name, role_description)

    execute_query(conn, sql)
    return 'Role was added Successfully'


# PUT method for roles
@app.route('/update_role', methods=['PUT'])
def update_role():
    # The user input is gathered in JSON format and stored into an empty variable
    role_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    Role_ID = role_data['Role_ID']
    # The JSON object is then separated into variables so that they may be used in a sql query
    Role_Name = role_data['Role_Name']
    Role_Description = role_data['Role_Description']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE roles SET Role_Name = %s, Role_Description = %s WHERE Role_ID = %s"
    val = (Role_Name, Role_Description, Role_ID)

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
    return customers


@app.route('/addcustomers', methods=['POST'])
def add_customer():
    # The user input is gathered in JSON format and stored into an empty variable
    customer_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    business_name = customer_data['business_name']
    business_hrs = customer_data['business_hrs']
    last_name = customer_data['last_name']
    first_name = customer_data['first_name']
    cust_acc_num = customer_data['cust_acc_num']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO customers(business_name, business_hrs, last_name, first_name, cust_acc_num) VALUES ('%s', '%s', '%s', '%s', %s')" % (
        business_name, business_hrs, last_name, first_name, cust_acc_num)

    execute_query(conn, sql)
    return 'Customer was added Successfully'


# PUT method for customers
@app.route('/update_customer', methods=['PUT'])
def update_customer():
    # The user input is gathered in JSON format and stored into an empty variable
    customer_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    customer_id = customer_data['customer_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    business_name = customer_data['business_name']
    business_hrs = customer_data['business_hrs']
    last_name = customer_data['last_name']
    first_name = customer_data['first_name']
    cust_acc_num = customer_data['cust_acc_num']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE customers SET business_name = %s, business_hrs = %s, last_name = %s, first_name = %s, cust_acc_num = %s WHERE customer_id = %s"
    val = (business_name, business_hrs, last_name,
           first_name, cust_acc_num, customer_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Customer was updated successfully'


##################################### CUSTOMERS CONTACTS ###################################

# Customer Contact Table CRUD


@app.route('/customer_contact', methods=['GET'])
def get_customer_contact():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """SELECT c.Customer_ID, c.Business_Name, c.First_Name, c.Last_Name, cc.Phone, cc.Email, cc.Street, cc.City cc.Zipcode 
                FROM Customers c 
                JOIN Customer_Contact cc ON c.Customer_ct_id = cc.Customer_ct_id        
                JOIN States s ON cc.state_code_id = s.State_Code_ID;_ct_id;"""
    customer_contact = execute_read_query(conn, sql)
    return customer_contact


@app.route('/addcustomercontact', methods=['POST'])
def add_customer_contact():
    # The user input is gathered in JSON format and stored into an empty variable
    employee_contact_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    phone = employee_contact_data['phone']
    email = employee_contact_data['email']
    street = employee_contact_data['street']
    city = employee_contact_data['city']
    state = employee_contact_data['state_code_id']
    zipcode = employee_contact_data['Zipcode']
    customer_id = employee_contact_data['customer_id']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO customer_contact(phone, email, street, city, state_code_id, Zipcode, customer_id ) VALUES (%s, '%s', '%s', '%s', '%s', %s, %s)" % (
        phone, email, street, city, state, zipcode, customer_id)

    execute_query(conn, sql)
    return 'Customer Contact was added Successfully'


# PUT method for customer contact
@app.route('/update_customer_contact', methods=['PUT'])
def update_customer_contact():
    # The user input is gathered in JSON format and stored into an empty variable
    customer_contact_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    customer_id = customer_contact_data['customer_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    Phone = customer_contact_data['Phone']
    Email = customer_contact_data['Email']
    Street = customer_contact_data['Street']
    City = customer_contact_data['City']
    state_code_id = customer_contact_data['state_code_id']
    Zipcode = customer_contact_data['Zipcode']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE customer_contact SET Phone = %s, Email = %s, Street = %s, City = %s, state_code_id = %s, Zipcode = %s WHERE customer_id = %s"
    val = (Phone, Email, Street, City, state_code_id, Zipcode, customer_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Customer contact was updated successfully'


############################# VENDORS ###################################

# Vendors Table CRUD


@app.route('/vendors', methods=['GET'])
def get_vendors():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM vendors"
    vendors = execute_read_query(conn, sql)
    return vendors


@app.route('/addvendor', methods=['POST'])
def add_vendor():
    # The user input is gathered in JSON format and stored into an empty variable
    vendor_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    vendor_name = vendor_data['vendor_name']
    vendor_hrs = vendor_data['vendor_hrs']
    vendor_account_number = vendor_data['vendor_account_number']
    vendor_ct_id = vendor_data['vendor_ct_id']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO vendors(vendor_name, vendor_hrs, vendor_account_number, vendor_ct_id) VALUES ('%s', '%s', %s, %s)" % (
        vendor_name, vendor_hrs, vendor_account_number, vendor_ct_id)

    execute_query(conn, sql)
    return 'Vendor was added Successfully'


# PUT method for vendors
@app.route('/update_vendor', methods=['PUT'])
def update_vendor():
    # The user input is gathered in JSON format and stored into an empty variable
    vendor_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    vendor_id = vendor_data['vendor_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    vendor_name = vendor_data['vendor_name']
    vendor_hrs = vendor_data['vendor_hrs']
    vendor_account_number = vendor_data['vendor_account_number']
    vendor_ct_id = vendor_data['vendor_ct_id']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE vendors SET vendor_name = %s, vendor_hrs = %s, vendor_account_number = %s, vendor_ct_id = %s WHERE vendor_id = %s"
    val = (vendor_name, vendor_hrs,
           vendor_account_number, vendor_ct_id, vendor_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Vendor was updated successfully'

############################# VENDORS CONTACT ###################################

# Vendor Contact Table


@app.route('/vendor_contact', methods=['GET'])
def get_vendor_contact():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """SELECT v.vendor_name, v.vendor_hrs, vc.phone, vc.email, vc.street, vc.city, vc.zipcode, s.state_code_id
            FROM vendors v
            JOIN vendor_contacts vc
            ON v.vendor_ct_id = vc.vendor_ct_id
            JOIN states sON vc.state_code_id = s.state_code_id"""
    vendor_contact = execute_read_query(conn, sql)
    return vendor_contact


@app.route('/addvendorcontact', methods=['POST'])
def add_vendor_contact():
    # The user input is gathered in JSON format and stored into an empty variable
    vendor_contact_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    phone = vendor_contact_data['phone']
    email = vendor_contact_data['email']
    street = vendor_contact_data['street']
    city = vendor_contact_data['city']
    state = vendor_contact_data['state_code_id']
    zipcode = vendor_contact_data['zipcode']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO vendor_contacts(phone, email, street, city, state_code_id, zipcode) VALUES (%s, '%s', '%s', '%s', '%s', %s)" % (
        phone, email, street, city, state, zipcode)

    execute_query(conn, sql)
    return 'Vendor Contact was added Successfully'


# PUT method for vendors contact
@app.route('/update_vendor_contact', methods=['PUT'])
def update_vendor_contact():
    # The user input is gathered in JSON format and stored into an empty variable
    vendor_contact_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    vendor_ct_id = vendor_contact_data['vendor_ct_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    phone = vendor_contact_data['phone']
    email = vendor_contact_data['email']
    street = vendor_contact_data['street']
    city = vendor_contact_data['city']
    state_code_id = vendor_contact_data['state_code_id']
    zipcode = vendor_contact_data['zipcode']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE vendor_contacts SET phone = %s, email = %s, street = %s, city = %s, state_code_id = %s, zipcode = %s WHERE vendor_ct_id = %s"
    val = (phone, email, street, city, state_code_id, zipcode, vendor_ct_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Vendor Contact was updated successfully'


############################# INVENTORY ###################################

# Inventory Table CRUD

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


@app.route('/addinventory', methods=['POST'])
def add_inventory():
    # The user input is gathered in JSON format and stored into an empty variable
    inventory_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    vendor_id = inventory_data['vendor_id']
    item_name = inventory_data['item_name']
    item_amount = inventory_data['item_amount']
    unit_cost = inventory_data['unit_cost']
    total_inv_cost = inventory_data['total_inv_cost']
    date_bought = inventory_data['date_bought']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO inventory(vendor_id, item_name, item_amount, unit_cost, total_inv_cost, date_bought) VALUES (%s, '%s', %s, %s, %s, %s)" % (
        vendor_id, item_name, item_amount, unit_cost, total_inv_cost, date_bought)

    execute_query(conn, sql)
    return 'Inventory was added Successfully'


# PUT method for inventory
@app.route('/update_inventory', methods=['PUT'])
def update_inventory():
    # The user input is gathered in JSON format and stored into an empty variable
    inventory_contact_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    inventory_id = inventory_contact_data['inventory_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    vendor_id = inventory_contact_data['vendor_id']
    item_name = inventory_contact_data['item_name']
    item_amount = inventory_contact_data['item_amount']
    unit_cost = inventory_contact_data['unit_cost']
    total_inv_cost = inventory_contact_data['total_inv_cost']
    date_bought = inventory_contact_data['date_bought']

    # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    fmt_date_bought = str(datetime.strptime(date_bought, '%m-%d-%Y').date())

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE inventory SET vendor_id = %s, item_name = %s, item_amount = %s, unit_cost = %s, total_inv_cost = %s, date_bought = %s WHERE inventory_id = %s"
    val = (vendor_id, item_name, item_amount, unit_cost,
           total_inv_cost, fmt_date_bought, inventory_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Inventory was updated successfully'


############################# PRODUCTS ###################################

# Products Table CRUD

@app.route('/products', methods=['GET'])
def get_products():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM products"
    products = execute_read_query(conn, sql)
    return products


@app.route('/addproduct', methods=['POST'])
def add_product():
    # The user input is gathered in JSON format and stored into an empty variable
    product_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    product_name = product_data['product_name']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO products(product_name) VALUES ('%s')" % (
        product_name)

    execute_query(conn, sql)
    return 'Product was added Successfully'


# PUT method for products
@app.route('/update_product', methods=['PUT'])
def update_product():
    # The user input is gathered in JSON format and stored into an empty variable
    products_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    product_id = products_data['product_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    product_name = products_data['product_name']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE products SET product_name = %s WHERE product_id = %s"
    val = (product_name, product_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Product was updated successfully'


############################# LINE ITEMS ########################################

# Line Items Table CRUD

@app.route('/lineitems', methods=['GET'])
def get_line_items():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM line_items"
    line_items = execute_read_query(conn, sql)
    return line_items


@app.route('/addlineitem', methods=['POST'])
def add_line_item():
    # The user input is gathered in JSON format and stored into an empty variable
    line_item_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    order_id = line_item_data['order_id']
    product_id = line_item_data['product_id']
    quantity = line_item_data['quantity']
    price_per_unit = line_item_data['price_per_unit']
    total = line_item_data['total']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO line_items(order_id, product_id, quantity, price_per_unit, total) VALUES (%s, %s, %s, %s, %s)" % (
        order_id, product_id, quantity, price_per_unit, total)

    execute_query(conn, sql)
    return 'Line Item was added Successfully'


# PUT method for products
@app.route('/update_line_item', methods=['PUT'])
def update_line_item():
    # The user input is gathered in JSON format and stored into an empty variable
    line_item_data = request.get_json()
    # we will be using employee_id to reference the entry to update
    item_id = line_item_data['item_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    order_id = line_item_data['order_id']
    product_id = line_item_data['product_id']
    quantity = line_item_data['quantity']
    price_per_unit = line_item_data['price_per_unit']
    total = line_item_data['total']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE line_items SET order_id = %s, product_id = %s, quantity = %s, price_per_unit = %s, total = %s WHERE item_id = %s"
    val = (order_id, product_id, quantity, price_per_unit, total, item_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Line Item was updated successfully'


############################# ORDERS ########################################

# Orders Table CRUD

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM orders"
    orders = execute_read_query(conn, sql)
    return orders


@app.route('/addorder', methods=['POST'])
def add_order():
    # The user input is gathered in JSON format and stored into an empty variable
    order_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    invoice_id = order_data['invoice_id']
    date_produced = order_data['date_produced']
    delivery_date = order_data['delivery_date']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO orders(invoice_id, date_produced, delivery_date) VALUES (%s, %s, %s)" % (
        invoice_id, date_produced, delivery_date)

    execute_query(conn, sql)
    return 'Order was added Successfully'

############################# INVOICES ######################################

# Invoices Table CRUD


@app.route('/invoices', methods=['GET'])
def get_invoices():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM invoices"
    invoices = execute_read_query(conn, sql)
    return invoices


@app.route('/addinvoice', methods=['POST'])
def add_invoice():
    # The user input is gathered in JSON format and stored into an empty variable
    invoice_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    vendor_id = invoice_data['vendor_id']
    customer_id = invoice_data['customer_id']
    invoice_number = invoice_data['invoice_number']
    invoice_date = invoice_data['invoice_date']
    invoice_total = invoice_data['invoice_total']
    payment_status = invoice_data['payment_status']
    date_paid = invoice_data['date_paid']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO invoices(vendor_id, customer_id, invoice_number, invoice_date, invoice_total, payment_status, date_paid) VALUES (%s, %s, %s, %s, %s, '%s', %s)" % (
        vendor_id, customer_id, invoice_number, invoice_date, invoice_total, payment_status, date_paid)

    execute_query(conn, sql)
    return 'Invoice was added Successfully'


############################# MAINTENENCE ###################################

# Garage Table CRUD

@app.route('/garage', methods=['GET'])
def get_garage():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM garage"
    garage = execute_read_query(conn, sql)
    return garage


@app.route('/addgarage', methods=['POST'])
def add_garage():
    # The user input is gathered in JSON format and stored into an empty variable
    garage_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    garage_name = garage_data['garage_name']
    phone_number = garage_data['phone_number']
    street = garage_data['street']
    city = garage_data['city']
    state = garage_data['state_code_id']
    zipcode = garage_data['zipcode']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO garage(garage_name, phone_number, street, city, state, zipcode) VALUES ('%s', %s, '%s', '%s', '%s', %s)" % (
        garage_name, phone_number, street, city, state, zipcode)

    execute_query(conn, sql)
    return 'Garage was added Successfully'


# Vehicle Table CRUD

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM vehicles"
    vehicles = execute_read_query(conn, sql)
    return vehicles


@app.route('/addvehicle', methods=['POST'])
def add_vehicle():
    # The user input is gathered in JSON format and stored into an empty variable
    vehicle_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    license_plate = vehicle_data['license_plate']
    make = vehicle_data['make']
    model = vehicle_data['model']
    vin = vehicle_data['vin']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO vehicles(license_plate, make, model, vin) VALUES ('%s', '%s', '%s', '%s')" % (
        license_plate, make, model, vin)

    execute_query(conn, sql)
    return 'Vehicle was added Successfully'


# Maintenance_Logs Table CRUD


# maintenance get method working now
# adjust sql as needed - Misael
@app.route('/maintenance', methods=['GET'])
def get_maintenance():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT * FROM maintenance_logs"
    maintenance = execute_read_query(conn, sql)
    return maintenance


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
    sql = "INSERT INTO maintenance_logs(garage_id, vehicle_id, date, status, note) VALUES (%s, %s, %s, '%s', '%s')" % (
        garage_id, vehicle_id, date, status, note)

    execute_query(conn, sql)
    return 'Maintenance Log was added Successfully'


app.run()
