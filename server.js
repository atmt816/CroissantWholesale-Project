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
app.get('/', function (req, res) {

    res.render('pages/index');
});

app.get('/login', function (req, res) {

    res.render('pages/login');
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

    // ORDER PAGE

    // app.get('/orders', function (req, res) {
    //     axios.get('http://127.0.0.1:5000/orders')
    //         .then((response) => {
    //             var order_data = response.data

    //             res.render('pages/orders',
    //                 {
    //                     order_data: order_data[0],
    //                     customers: order_data[2],
    //                     products: order_data[4]
    //                 });
    //         });
    // });


    app.post('/addorder', function (req, res) {
        axios.post('http://127.0.0.1:5000/addorder',
            {
                first_name: req.body.first_name,
                customer_id: req.body.customer_id,
                delivery_date: req.body.delivery_date,
                delivery_phone: req.body.delivery_phone,
                delivery_street: req.body.delivery_street,
                delivery_city: req.body.delivery_city,
                state_code_id: req.body.state_code_id,
                zipcode: req.body.zipcode,
                line_items: req.body.line_items
            }
        )
            .then((response) => {
                axios.get('http://127.0.0.1:5000/orders')
                    .then((response, states) => {
                        var order_data = response.data

                        res.render('pages/orders',
                            {
                                order_data: order_data[0],
                                states: order_data[1],
                                customers: order_data[2],
                                products: order_data[3]
                            });
                    });
            });
    });


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
            customer_id : req.body.customer_id,
            status : req.body.status,
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





app.listen(3000);
console.log('3000 is the magic port');
