// load the things we need
var express = require('express');
var app = express();
const bodyParser = require('body-parser');
// required module to make calls to a REST API
const axios = require('axios');
const { response } = require('express');
const req = require('express/lib/request');
const { type } = require('express/lib/response');
var selectedID = "";
app.use(bodyParser.urlencoded());
app.set('view engine', 'ejs');

// set the view engine to ejs

app.set('view engine', 'ejs');
/*app.get('/home', function (req, res) {

    res.render('pages/home');
});*/

app.get('/', function (req, res) {

    res.render('pages/login');
});

app.get('/login', function (req, res) {

    res.render('pages/login');
});

app.get('/logged_out', function (req, res) {

    res.render('pages/logged_out');
});

// EMPLOYEE PAGE 

app.get('/employees', function (req, res) {
    axios.get('http://127.0.0.1:5000/employees')
        .then((response, states) => {
            // console.log(response.data)
            var employee_data = response.data

            res.render('pages/employees',
                {
                    employee_data: employee_data[0],
                    states: employee_data[1],
                    roles: employee_data[2]
                });
        });
});


app.get('/empinfo/:id', function (req, res) {
    const emp_id = req.params.id;

    axios.get('http://127.0.0.1:5000/employees/' + emp_id
    ).then((response, states) => {
        var employee_data = response.data

        res.render('pages/empinfo',
            {
                employee_data: employee_data[0],
                states: employee_data[1],
                roles: employee_data[2]
            });
    });

});


app.post('/employees/add', function (req, res) {
    axios.post('http://127.0.0.1:5000/employees/add',
        {
            first_name: req.body.first_name,
            last_name: req.body.last_name,
            start_date: req.body.start_date,
            emp_status: req.body.emp_status,
            role_id: req.body.role_id,
            phone: req.body.phone,
            email: req.body.email,
            street: req.body.street,
            city: req.body.city,
            state_code_id: req.body.states,
            zipcode: req.body.zipcode

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/employees')
                .then((response, states) => {
                    // console.log(response.data)
                    var employee_data = response.data

                    res.render('pages/employees',
                        {
                            employee_data: employee_data[0],
                            states: employee_data[1],
                            roles: employee_data[2]
                        });
                });
        });
});

app.post('/employees/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_employee/',
        {
            emp_id: req.body.emp_id,
            first_name: req.body.first_name,
            last_name: req.body.last_name,
            start_date: req.body.start_date,
            end_date: req.body.end_date,
            emp_status: req.body.emp_status,
            role_id: req.body.role_id,
            phone: req.body.phone,
            email: req.body.email,
            street: req.body.street,
            city: req.body.city,
            state_code_id: req.body.states,
            zipcode: req.body.zipcode

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/employees')
                .then((response, states) => {
                    // console.log(response.data)
                    var employee_data = response.data

                    res.render('pages/employees',
                        {
                            employee_data: employee_data[0],
                            states: employee_data[1],
                            roles: employee_data[2]
                        });
                });
        }

        );
});


// ROLES PAGE
app.get('/roles', function (req, res) {
    axios.get('http://127.0.0.1:5000/roles')
        .then((response, states) => {

            var roles_data = response.data

            res.render('pages/roles',
                {
                    roles_data: roles_data

                });
        });
});


app.post('/roles/add', function (req, res) {
    axios.post('http://127.0.0.1:5000/addrole',
        {
            role_name: req.body.role_name,
            role_description: req.body.role_description,
            role_status: req.body.role_status

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/roles')
                .then((response, states) => {
                    // console.log(response.data)
                    var roles_data = response.data

                    res.render('pages/roles',
                        {
                            roles_data: roles_data

                        });
                });
        });
});

app.get('/rolesinfo', function (req, res) {

    res.render('pages/rolesinfo');
});

app.get('/rolesinfo/:id', function (req, res) {
    const role_id = req.params.id;

    axios.get('http://127.0.0.1:5000/roles/' + role_id
    ).then((response, states) => {
        var roles_data = response.data

        res.render('pages/rolesinfo',
            {
                roles_data: roles_data[0]
            });
    });

});


app.post('/roles/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_role',
        {
            role_id: req.body.role_id,
            role_name: req.body.role_name,
            role_description: req.body.role_description,
            role_status: req.body.role_status

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/roles')
                .then((response, states) => {
                    // console.log(response.data)
                    var roles_data = response.data

                    res.render('pages/roles',
                        {
                            roles_data: roles_data

                        });
                });
        }

        );
});


// CUSTOMER PAGE


app.get('/customers', function (req, res) {
    axios.get('http://127.0.0.1:5000/customers')
        .then((response, states) => {

            var customer_data = response.data

            res.render('pages/customers',
                {
                    customer_data: customer_data[0],
                    states: customer_data[1]
                });
        });
});

app.get('/custinfo/:id', function (req, res) {
    const customer_id = req.params.id;


    axios.get('http://127.0.0.1:5000/customers/' + customer_id
    ).then((response, states) => {
        var customer_data = response.data

        res.render('pages/custinfo',
            {
                customer_data: customer_data[0],
                states: customer_data[1]

            });
    });

});

app.post('/customers/add', function (req, res) {
    axios.post('http://127.0.0.1:5000/customers/add',
        {
            business_name: req.body.business_name,
            business_hrs: req.body.business_hrs,
            last_name: req.body.last_name,
            first_name: req.body.first_name,
            cust_acc_num: req.body.cust_acc_num,
            customer_status: req.body.customer_status,
            Phone: req.body.Phone,
            Email: req.body.Email,
            Street: req.body.Street,
            City: req.body.City,
            state_code_id: req.body.states,
            Zipcode: req.body.Zipcode

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/customers')
                .then((response, states) => {
                    // console.log(response.data)
                    var customer_data = response.data

                    res.render('pages/customers',
                        {
                            customer_data: customer_data[0],
                            states: customer_data[1]
                        });
                });
        });
});

app.post('/customers/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_customer/',
        {
            customer_id: req.body.customer_id,
            business_name: req.body.business_name,
            business_hrs: req.body.business_hrs,
            last_name: req.body.last_name,
            first_name: req.body.first_name,
            cust_acc_num: req.body.cust_acc_num,
            customer_status: req.body.customer_status,
            phone: req.body.phone,
            email: req.body.email,
            street: req.body.street,
            city: req.body.city,
            state_code_id: req.body.states,
            zipcode: req.body.zipcode

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/customers')
                .then((response, states) => {
                    // console.log(response.data)
                    var customer_data = response.data

                    res.render('pages/customers',
                        {
                            customer_data: customer_data[0],
                            states: customer_data[1]

                        });
                });
        }

        );
});

//VENDORS PAGE
app.get('/vendors', function (req, res) {
    axios.get('http://127.0.0.1:5000/vendors')
        .then((response, states) => {
            // console.log(response.data)
            var vendor_data = response.data

            res.render('pages/vendors',
                {
                    vendor_data: vendor_data[0],
                    states: vendor_data[1]
                });
        });
});

app.get('/vendinfo/:id', function (req, res) {
    const vendor_id = req.params.id;


    axios.get('http://127.0.0.1:5000/vendors/' + vendor_id
    ).then((response, states) => {
        var vendor_data = response.data

        res.render('pages/vendinfo',
            {
                vendor_data: vendor_data[0],
                states: vendor_data[1]
            });
    });

});

app.post('/vendors/add', function (req, res) {
    axios.post('http://127.0.0.1:5000/vendors/add',
        {
            vendor_name: req.body.vendor_name,
            vendor_hrs: req.body.vendor_hrs,
            vendor_account_number: req.body.vendor_account_number,
            vendor_status: req.body.vendor_status,
            phone: req.body.phone,
            email: req.body.email,
            street: req.body.street,
            city: req.body.city,
            state_code_id: req.body.states,
            zipcode: req.body.zipcode

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/vendors')
                .then((response, states) => {
                    // console.log(response.data)
                    var vendor_data = response.data

                    res.render('pages/vendors',
                        {
                            vendor_data: vendor_data[0],
                            states: vendor_data[1],
                            roles: vendor_data[2]
                        });
                });
        });
});

app.post('/vendors/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_vendor/',
        {
            vendor_id: req.body.vendor_id,
            vendor_name: req.body.vendor_name,
            vendor_hrs: req.body.vendor_hrs,
            vendor_account_number: req.body.vendor_account_number,
            vendor_status: req.body.vendor_status,
            phone: req.body.phone,
            email: req.body.email,
            street: req.body.street,
            city: req.body.city,
            state_code_id: req.body.states,
            zipcode: req.body.zipcode

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/vendors')
                .then((response, states) => {
                    // console.log(response.data)
                    var vendor_data = response.data

                    res.render('pages/vendors',
                        {
                            vendor_data: vendor_data[0],
                            states: vendor_data[1]

                        });
                });
        }

        );
});



//ORDERS PAGE

app.get('/orders', function (req, res) {
    axios.get('http://127.0.0.1:5000/orders')
        .then((response) => {
            var order_data = response.data

            res.render('pages/orders',
                {
                    order_data: order_data[0],
                    customers: order_data[1],
                    products: order_data[2],
                    line_items: order_data[3]
                });
        });
});



app.post('/orders/add', function (req, res) {
    axios.post('http://127.0.0.1:5000/addorder',
        {
            customer_id: req.body.customer_id,
            status: req.body.status,
            line_items: req.body.line_items

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/orders')
                .then((response, states) => {
                    // console.log(response.data)
                    var order_data = response.data

                    res.render('pages/orders',
                        {
                            order_data: order_data[0],
                            customers: order_data[1],
                            products: order_data[2],
                            line_items: order_data[3]
                        });
                });
        });
});

app.get('/ordersinfo/:id', function (req, res) {
    const order_id = req.params.id;


    axios.get('http://127.0.0.1:5000/orders/' + order_id
    ).then((response, states) => {
        var order_data = response.data
        var obj = order_data[4]
        var sumtotal = parseInt(obj[0]["sum(total)"]);


        res.render('pages/ordersinfo',
            {
                order_data: order_data[0],
                customer_data: order_data[1],
                product_data: order_data[2],
                customers_data: order_data[3],
                total: order_data[4],
                sumtotal: sumtotal

            });
    });

});


app.post('/orders/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_order',
        {
            order_id: req.body.order_id,
            customer_id: req.body.customer_id,
            status: req.body.status,
            delivery_date: req.body.delivery_date,
            line_items: req.body.line_items

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/orders')
                .then((response, states) => {
                    // console.log(response.data)
                    var order_data = response.data

                    res.render('pages/orders',
                        {
                            order_data: order_data[0],
                            customers: order_data[1],
                            products: order_data[2],
                            line_items: order_data[3]
                        });
                });
        }

        );
});

app.post('/ordersinfo/:id', function (req, res) {
    const order_id = req.params.id;


    axios.delete('http://127.0.0.1:5000/orders/' + order_id
    ).then((response, states) => {
        res.render('pages/orders',
            {
                order_data: order_data[0],
                customers: order_data[1],
                products: order_data[2],
                line_items: order_data[3]
            });
    });

});

app.get('/inventory', function (req, res) {
    axios.get('http://127.0.0.1:5000/inventory')
        .then((response) => {
            var inventory_data = response.data
            console.log(inventory_data)
            res.render('pages/inventory',
                {
                    inventory_data: inventory_data[0],
                    vendors: inventory_data[1]
                });
        });
});

app.post('/inventory/add', function (req, res) {
    axios.post('http://127.0.0.1:5000/inventory/add',
        {
            vendor_id: req.body.vendor_id,
            item_name: req.body.item_name,
            item_amount: req.body.item_amount,
            unit_cost: req.body.unit_cost,
            total_inv_cost: req.body.total_inv_cost,
            date_bought: req.body.date_bought

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/inventory')
                .then((response, states) => {
                    // console.log(response.data)
                    var inventory_data = response.data

                    res.render('pages/inventory',
                        {
                            inventory_data: inventory_data[0],
                            vendors: inventory_data[1]

                        });
                });
        });
});

app.get('/inveninfo/:id', function (req, res) {
    const inventory_id = req.params.id;

    axios.get('http://127.0.0.1:5000/inveninfo/' + inventory_id
    ).then((response, states) => {
        var inventory_data = response.data

        res.render('pages/inveninfo',
            {
                inventory_data: inventory_data[0],
                vendors: inventory_data[1]
            });
    });

});

app.post('/inventory/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_inventory',
        {
            inventory_id: req.body.inventory_id,
            vendor_id: req.body.inventory_id,
            item_name: req.body.item_name,
            item_amount: req.body.item_amount,
            unit_cost: req.body.unit_cost,
            // total_inv_cost: req.body.total_inv_cost,
            date_bought: req.body.date_bought

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/inventory')
                .then((response, states) => {
                    // console.log(response.data)
                    var inventory_data = response.data

                    res.render('pages/inventory',
                        {
                            inventory_data: inventory_data[0],
                            vendors: inventory_data[1]

                        });
                });
        }

        );
});


app.get("/home", async (req, res, next) => {

    let chartApi;
    let weekly_data;
    let vendinv_data;
    let prodcount_data;

    try {
        chartApi = await axios.get("http://127.0.0.1:5000/monthlyordercount")
        weekly_data = await axios.get('http://127.0.0.1:5000/weeklyfulfillmentreport')
        vendinv_data = await axios.get('http://127.0.0.1:5000/vendorinventoryreport')
        prodcount_data = await axios.get('http://127.0.0.1:5000/productcounter')

    } catch (err) {
        console.error(err);
        return res.end('err');
    }

    res.render('pages/chart',
        {
            chartApi: chartApi.data,
            weekly_data: weekly_data.data,
            vendinv_data: vendinv_data.data,
            prodcount_data: prodcount_data.data
        });

});


app.listen(3000);
console.log('3000 is the magic port');
