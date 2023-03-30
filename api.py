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
from flask import render_template
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

# employees get method working now
# not returning data for now since roles table is empty
# adjust sql as needed - Misael

# GET method for employees


@app.route('/employees', methods=['GET'])
def employee():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """
        SELECT e.emp_id, e.first_name, e.last_name, e.start_date, e.end_date, e.emp_status, r.role_name
        FROM employees AS e
        JOIN roles AS r
        ON e.role_id = r.role_id
        ORDER BY e.emp_status ASC
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


# Get employee info by id
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
    fmt_start_date = str(datetime.strptime(start_date, '%m-%d-%Y').date())

    fmt_end_date = "null"
    if end_date != "null" and end_date != "NULL":
        fmt_end_date = str(datetime.strptime(end_date, '%m-%d-%Y').date())

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    # update employees table
    cursor = conn.cursor()
    sql = "UPDATE employees SET first_name = %s, last_name = %s, start_date = %s, end_date = %s, emp_status = %s, role_id = %s WHERE emp_id = %s"
    val = (first_name, last_name,
           fmt_start_date, fmt_end_date, emp_status, role_id, emp_id)
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
    phone = request_data['Phone']
    email = request_data['Email']
    street = request_data['Street']
    city = request_data['City']
    state_code_id = request_data['state_code_id']
    zipcode = request_data['Zipcode']

    sql = """
    INSERT INTO customers (business_name, business_hrs, last_name, first_name, cust_acc_num, customer_status) VALUES ('%s', '%s', '%s', '%s', %s, '%s')
    """ % (business_name, business_hrs, last_name, first_name, cust_acc_num, customer_status)

    execute_query(conn, sql)

    # gets the customer id from the above execution
    sql = 'SELECT * FROM customers WHERE customer_id= LAST_INSERT_ID()'
    customer_id = execute_read_query(conn, sql)
    customer_id = customer_id[0]['customer_id']
    # customer_id = request_data['customer_id']

    sql = """INSERT INTO customer_contact(customer_id,  Phone, Email, Street, City, state_code_id, Zipcode ) VALUES (%s, %s, '%s', '%s', '%s', '%s', %s)""" % (
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
    sql = "UPDATE customer_contact SET phone = %s, email = %s, street = %s, city = %s, state_code_id = %s, zipcode = %s WHERE customer_id = %s"
    val = (phone, email, street, city, state, zipcode, customer_id)

    cursor.execute(sql, val)

    conn.commit()
    return 'Customer was updated successfully'

############################# VENDORS ###################################

# Vendors Table CRUD


# @app.route('/vendors', methods=['GET'])
# def get_vendors():
#     conn = create_connection(
#         'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
#     sql = "SELECT * FROM vendors"
#     vendors = execute_read_query(conn, sql)

#     sql = """
#         SELECT * FROM states;
#         """
#     states = execute_read_query(conn, sql)

#     sql = """
#         SELECT * FROM roles;
#         """
#     roles = execute_read_query(conn, sql)

#    return jsonify(vendors, states, roles)


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


# Vendor Inventory Report - report generates a list of all inventory items, grouped by the vendor id the items are procured from.


@app.route('/vendorinventoryreport', methods=['GET'])
def get_vendor_inv_sheet():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT v.Vendor_ID, ii.Inventory_id, v.Vendor_Name, ii.Item_Name, ii.Item_Amount, ii.Unit_Cost ii.Total_Inv_Cost, ii.Last_Updated FROM Vendors AS v JOIN Inventory AS ii ON v.Vendor_ID = ii.Vendor_ID GROUP BY v.Vendor_ID;"
    vendor_inv_sheet = execute_read_query(conn, sql)
    return vendor_inv_sheet


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
    # we will be using inventory_id to reference the entry to update
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
    # we will be using product_id to reference the entry to update
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
    # we will be using item_id to reference the entry to update
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
    sql = "SELECT * FROM orders;"
    orders = execute_read_query(conn, sql)
    sql = """
         SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)
    sql = """
         SELECT * FROM customers;
        """
    customers = execute_read_query(conn, sql)
    sql = """
         SELECT * FROM customer_contact;
        """
    customer_contact = execute_read_query(conn, sql)
    sql = """
         SELECT * FROM products;
        """
    products = execute_read_query(conn, sql)

    return jsonify(orders, states, customers, customer_contact, products)


@app.route('/customerorderinfo/<customer_id>', methods=['GET'])
def get_customer_order_info(customer_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """
        SELECT * FROM customer_contact
        WHERE customer_id = '%s';
        """ % (customer_id)

    customer_order_info = execute_read_query(conn, sql)
    # print(sql)
    sql = """
         SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)

    sql = """ SELECT * FROM roles;"""
    roles = execute_read_query(conn, sql)

    return jsonify(customer_order_info, states, roles)


@app.route('/getcustomerid/<business_name>', methods=['GET'])
def get_customer_id(business_name):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """
        SELECT customer_id FROM customers
        WHERE business_name = '%s';
        """ % (business_name)

    get_customer_id = execute_read_query(conn, sql)

    return jsonify(get_customer_id)


@app.route('/addorder', methods=['POST'])
def add_order():
    # The user input is gathered in JSON format and stored into an empty variable
    order_data = request.get_json()
    # The JSON object is then separated into variables so that they may be used in a sql query
    sql = """
         SELECT CURDATE;
        """
    date_produced = execute_read_query(conn, sql)

    customer_id = order_data['customer_id']
    delivery_date = order_data['delivery_date']
    delivery_phone = order_data['delivery_phone']
    delivery_street = order_data['delivery_street']
    delivery_city = order_data['delivery_city']
    state_code_id = order_data['state_code_id']
    zipcode = order_data['zipcode']
    line_items = order_data['line_items']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO orders(date_produced, delivery_date, delivery_phone, delivery_street, delivery_city, state_code_id, zipcode) VALUES (%s, %s, %s, '%s', '%s', '%s', %s)" % (
        date_produced, delivery_date, delivery_phone, delivery_street, delivery_city, state_code_id, zipcode)
    execute_query(conn, sql)

    # gets the order id from the above execution
    sql = 'SELECT * FROM orders WHERE order_id= LAST_INSERT_ID()'
    order_id = execute_read_query(conn, sql)
    order_id = order_id[0]['order_id']

    # Set up future invoice with corresponding ids
    sql = "INSERT INTO invoices(customer_id, order_id) VALUES (%s, %s)" % (
        customer_id, order_id)
    execute_query(conn, sql)

    cursor = conn.cursor()
    for product_id, items in line_items.items():
        for item in items:
            quantity = item['quantity']
            price_per_unit = item['price_per_unit']
            total = item['total']
            cursor.execute("INSERT INTO line_items (order_id, product_id, quantity, price_per_unit, total) VALUES (%s, %s, %s, %s, %s)",
                           (order_id, product_id, quantity, price_per_unit, total))
    conn.commit()

    return 'Order was added Successfully'


# Fulfillment Report
# Fulfillment check per line item. Report generates all orders within a timeframe that are scheduled for delivery.
# User can then ensure all items have been made to fulfill these orders, or plan accordingly if more ingredients must be ordered.

# Daily


@app.route('/dailyfulfillmentreport', methods=['GET'])
def get_daily_ful_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT O.Order_ID, O.Date_Produced, O.Delivery_Date, P.Product_ID, Product_Name, LI.Quantity FROM products AS P INNER JOIN line_items AS LI ON P.Product_ID = LI.Product_ID INNER JOIN orders as O ON O.Order_ID = LI.Order_ID WHERE O.Delivery_Date = curdate() GROUP BY O.Order_ID, O.Date_Produced, O.Delivery_Date"
    daily_ful_report = execute_read_query(conn, sql)
    return daily_ful_report

# Weekly


@app.route('/weeklyfulfillmentreport', methods=['GET'])
def get_weekly_ful_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT O.Order_ID, O.Date_Produced, O.Delivery_Date, P.Product_ID, Product_Name, LI.Quantity FROM products AS P INNER JOIN line_items AS LI ON P.Product_ID = LI.Product_ID INNER JOIN orders as O ON O.Order_ID = LI.Order_ID WHERE O.Delivery_Date BETWEEN curdate() AND curdate()+8 GROUP BY O.Order_ID, O.Date_Produced, O.Delivery_Date"
    weekly_ful_report = execute_read_query(conn, sql)
    return weekly_ful_report

# Monthly


@app.route('/monthlyfulfillmentreport', methods=['GET'])
def get_monthly_ful_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT O.Order_ID, O.Date_Produced, O.Delivery_Date, P.Product_ID, Product_Name, LI.Quantity FROM products AS P INNER JOIN line_items AS LI ON P.Product_ID = LI.Product_ID INNER JOIN orders as O ON O.Order_ID = LI.Order_ID WHERE O.Delivery_Date BETWEEN curdate() AND curdate()+30 GROUP BY O.Order_ID, O.Date_Produced, O.Delivery_Date"
    monthly_ful_report = execute_read_query(conn, sql)
    return monthly_ful_report


# Best Selling Items Report
# This report generates a count for each specific line item's frequency across all orders.

# Daily Best Sellers - Determine most popular items amongst all orders scheduled for delivery on current date.
@app.route('/dailybestsellers', methods=['GET'])
def get_daily_best_sell_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit, O.Order_ID, LI.Quantity, COUNT(O.Order_ID) AS Order_Frequency FROM orders AS O INNER JOIN line_items AS LI ON LI.Order_ID = O.Order_ID INNER JOIN products as P ON P.Product_ID = LI.Product_ID WHERE O.Delivery_Date = curdate() GROUP BY P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit"
    daily_best_sell_report = execute_read_query(conn, sql)
    return daily_best_sell_report

# Weekly Best Sellers - Determine most popular items amongst all orders scheduled for delivery within a week from the current date.


@app.route('/weeklybestsellers', methods=['GET'])
def get_weekly_best_sell_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit, O.Order_ID, LI.Quantity, COUNT(O.Order_ID) AS Order_Frequency FROM orders AS O INNER JOIN line_items AS LI ON LI.Order_ID = O.Order_ID INNER JOIN products as P ON P.Product_ID = LI.Product_ID WHERE O.Delivery_Date BETWEEN curdate() AND curdate()+8 GROUP BY P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit"
    weekly_best_sell_report = execute_read_query(conn, sql)
    return weekly_best_sell_report

# Monthly Best Sellers - Determine most popular items amongst all orders scheduled for delivery within a month from the current date.


@app.route('/monthlybestsellers', methods=['GET'])
def get_monthly_best_sell_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit, O.Order_ID, LI.Quantity, COUNT(O.Order_ID) AS Order_Frequency FROM orders AS O INNER JOIN line_items AS LI ON LI.Order_ID = O.Order_ID INNER JOIN products as P ON P.Product_ID = LI.Product_ID WHERE O.Delivery_Date BETWEEN curdate() AND curdate()+30 GROUP BY P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit"
    monthly_best_sell_report = execute_read_query(conn, sql)
    return monthly_best_sell_report

# Lifetime Best Sellers - Determine most popular items amongst all historical orders.


@app.route('/lifetimebestsellers', methods=['GET'])
def get_lifetime_best_sell_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit, O.Order_ID, LI.Quantity, COUNT(O.Order_ID) AS Order_Frequency FROM orders AS O INNER JOIN line_items AS LI ON LI.Order_ID = O.Order_ID INNER JOIN products as P ON P.Product_ID = LI.Product_ID GROUP BY P.Product_ID, P.Product_Name, LI.Item_ID, LI.Price_Per_Unit"
    lifetime_best_sell_report = execute_read_query(conn, sql)
    return lifetime_best_sell_report

# Orders-Invoice Report- View payment status of all orders with their corresponding invoice.


@app.route('/paymentstatus', methods=['GET'])
def get_payment_status_report():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT i.Customer_ID, o.Order_id, i.Invoice_Number, i.Invoice_date, i.Invoice_total, i.Payment_Status, i.Date_Paid FROM Invoices i JOIN Orders o ON i.Invoice_ID = o.Invoice_ID; "
    payment_status_report = execute_read_query(conn, sql)
    return payment_status_report

# Delivery Sheet Report - Generate a customer contact list for all deliveries scheduled on the current date.


@app.route('/deliverysheet', methods=['GET'])
def get_delivery_sheet():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT c.Customer_ID, c.Business_Name, c.First_Name, c.Last_Name, c.Customer_Account_Number, cc.Phone, cc.Street, cc.City, cc.Zipcode, o.Order_id, o.Delivery_date FROM Customers as c JOIN Customer_Contact AS cc ON c.Customer_ct_id = cc.Customer_ct_id JOIN Orders AS o ON cc.Order_Id = o. Orders_Id WHERE o.Delivery_Date = curdate();  "
    delivery_sheet = execute_read_query(conn, sql)
    return delivery_sheet

# PUT method for orders


@app.route('/update_order', methods=['PUT'])
def update_order():
    # The user input is gathered in JSON format and stored into an empty variable
    order_data = request.get_json()
    # we will be using order_id to reference the entry to update
    order_id = order_data['order_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    invoice_id = order_data['invoice_id']
    date_produced = order_data['date_produced']
    delivery_date = order_data['delivery_date']

    # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    fmt_date_produced = str(datetime.strptime(
        date_produced, '%m-%d-%Y').date())
    # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    fmt_delivery_date = str(datetime.strptime(
        delivery_date, '%m-%d-%Y').date())

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE orders SET invoice_id = %s, date_produced = %s, delivery_date = %s WHERE order_id = %s"
    val = (invoice_id, fmt_date_produced, fmt_delivery_date, order_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Order was updated successfully'

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
    customer_id = invoice_data['customer_id']
    invoice_number = invoice_data['invoice_number']
    invoice_date = invoice_data['invoice_date']
    invoice_total = invoice_data['invoice_total']
    payment_status = invoice_data['payment_status']
    date_paid = invoice_data['date_paid']
    order_id = order_id['order_id']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "INSERT INTO invoices(customer_id, customer_id, invoice_number, invoice_date, invoice_total, payment_status, date_paid, order_id) VALUES (%s, %s, %s, %s, %s, '%s', %s, %s)" % (
        customer_id, customer_id, invoice_number, invoice_date, invoice_total, payment_status, date_paid, order_id)

    execute_query(conn, sql)
    return 'Invoice was added Successfully'


# PUT method for invoices
@app.route('/update_invoices', methods=['PUT'])
def update_invoices():
    # The user input is gathered in JSON format and stored into an empty variable
    invoice_data = request.get_json()
    # we will be using invoice_id to reference the entry to update
    invoice_id = invoice_data['invoice_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    vendor_id = invoice_data['vendor_id']
    customer_id = invoice_data['customer_id']
    invoice_number = invoice_data['invoice_number']
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
    val = (vendor_id, customer_id, invoice_number, fmt_invoice_date,
           invoice_total, payment_status, fmt_date_paid, invoice_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Invoice was updated successfully'


############################# MAINTENENCE ###################################

# Garage Table CRUD

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

# Specifc garage id get for modal info


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


# PUT method for garage
@app.route('/update_garage', methods=['PUT'])
def update_garage():
    # The user input is gathered in JSON format and stored into an empty variable
    garage_data = request.get_json()
    # we will be using garage_id to reference the entry to update
    garage_id = garage_data['garage_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    garage_name = garage_data['garage_name']
    phone_number = garage_data['phone_number']
    street = garage_data['street']
    city = garage_data['city']
    state_code_id = garage_data['state_code_id']
    zipcode = garage_data['zipcode']

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE garage SET garage_name = %s, phone_number = %s, street = %s, city = %s, state_code_id = %s, zipcode = %s WHERE garage_id = %s"
    val = (garage_name, phone_number, street,
           city, state_code_id, zipcode, garage_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Garage was updated successfully'


# Vehicle Table CRUD

@app.route('/vehicles', methods=['GET'])
def get_vehicles_info():
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

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE vehicles SET license_plate = %s, make = %s, model = %s, vin = %s WHERE vehicle_id = %s"
    val = (license_plate, make, model, vin, vehicle_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Vehicle was updated successfully'

# Get specific vehicle info with maintenence log data for modal


@app.route('/vehicles/<vehicle_id>', methods=['GET'])
def get_vehicles(vehicle_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = """SELECT v.vehicle_id, v.license_plate, v.make, v.model, v.vin, ml.log_id, ml.date, ml.status, ml.note, g.garage_name, g.phone_number, g.street, g.city, s.state_code_id, g.zipcode
            FROM vehicles v
            JOIN maintenance_logs ml
            ON v.vehicle_id = ml.vehicle_id
            JOIN garage AS g
            ON ml.garage_id = g.garage_id
            JOIN states s
            ON g.state_code_id = s.state_code_id
        WHERE v.vehicle_id = '%s';""" % (vehicle_id)
    vehicles = execute_read_query(conn, sql)

    sql = """
         SELECT * FROM states;
        """
    states = execute_read_query(conn, sql)

    return jsonify(vehicles, states)


# Maintenance_Logs Table CRUD


# maintenance get method working now
# adjust sql as needed - Misael
@app.route('/maintenance', methods=['GET'])
def get_maintenance():
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT v.license_plate AS 'License Plate', g.garage_name AS 'Garage Name',logs.date AS 'Date', logs.status AS 'Status', logs.note AS 'note' FROM maintenance_logs AS logs INNER JOIN vehicles AS v ON logs.vehicle_id = v.vehicle_id INNER JOIN garage AS g ON logs.garage_id = g.garage_id ORDER BY date DESC;"
    maintenance = execute_read_query(conn, sql)
    return maintenance

# Specific maintenance log details for selected row


@app.route('/maintenance/<log_id>', methods=['GET'])
def get_maintenance_info(log_id):
    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')
    sql = "SELECT v.license_plate AS 'License Plate', g.garage_name AS 'Garage Name',logs.date AS 'Date', logs.status AS 'Status', logs.note AS 'note' FROM maintenance_logs AS logs INNER JOIN vehicles AS v ON logs.vehicle_id = v.vehicle_id INNER JOIN garage AS g ON logs.garage_id = g.garage_id ORDER BY date DESC WHERE logs.log_id = %s;" % (
        log_id)
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
    return vehicle_main_log


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
    return garage_main_log


# PUT method for maintenance_logs
@app.route('/update_maintenance_log', methods=['PUT'])
def update_maintenance_log():
    # The user input is gathered in JSON format and stored into an empty variable
    maintenance_data = request.get_json()
    # we will be using log_id to reference the entry to update
    log_id = maintenance_data['log_id']
    # The JSON object is then separated into variables so that they may be used in a sql query
    garage_id = maintenance_data['garage_id']
    vehicle_id = maintenance_data['vehicle_id']
    date = maintenance_data['date']
    status = maintenance_data['status']
    note = maintenance_data['note']

    # date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)
    fmt_date = str(datetime.strptime(date, '%m-%d-%Y').date())

    conn = create_connection(
        'cis4375.cfab8c2lm5ph.us-east-1.rds.amazonaws.com', 'admin', 'cougarcode', 'cid4375')

    cursor = conn.cursor()
    sql = "UPDATE maintenance_logs SET garage_id = %s, vehicle_id = %s, date = %s, status = %s, note = %s WHERE log_id = %s"
    val = (garage_id, vehicle_id, fmt_date, status, note, log_id)

    cursor.execute(sql, val)
    conn.commit()
    return 'Maintenance Log was updated successfully'


app.run()
