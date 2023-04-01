// load the things we need
var express = require('express');
var app = express();
const bodyParser = require('body-parser');
// required module to make calls to a REST API
const axios = require('axios');
const { response } = require('express');
const req = require('express/lib/request');
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


//Vehicles PAGE

app.get('/vehicles', function (req, res) {
    axios.get('http://127.0.0.1:5000/vehicles')
        .then((response, states) => {

            var vehicles_data = response.data

            res.render('pages/vehicles',
                {
                    vehicles_data: vehicles_data

                });
        });
});

app.post('/vehicles/add', function (req, res) {
    axios.post('http://127.0.0.1:5000/addvehicle',
        {
            license_plate: req.body.license_plate,
            make : req.body.make,
            model : req.body.model,
            vin : req.body.vin,
            status : req.body.status

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/vehicles')
                .then((response, states) => {
                    // console.log(response.data)
                    var vehicles_data = response.data

                    res.render('pages/vehicles',
                        {
                            vehicles_data: vehicles_data
                         
                        });
                });
        });
});

app.get('/vehiclesinfo/:id', function (req, res) {
    const vehicle_id = req.params.id;

    axios.get('http://127.0.0.1:5000/vehicles/' + vehicle_id
    ).then((response, states) => {
        var vehicles_data = response.data

        res.render('pages/vehiclesinfo',
            {
                vehicles_data: vehicles_data[0]
            });
    });

});

//Maintenance Page
app.get('/maintenance', function (req, res) {
    axios.get('http://127.0.0.1:5000/maintenance')
        .then((response, states) => {

            var logs_data = response.data

            res.render('pages/maintenance',
                {
                    logs_data: logs_data

                });
        });
});

app.post('/maintenance/addlog', function (req, res) {
    axios.post('http://127.0.0.1:5000/addmaintenancelog',
        {
            garage_id: req.body.garage_id,
            vehicle_id : req.body.vehicle_id,
            date : req.body.date,
            status : req.body.status,
            note : req.body.note

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/maintenance')
                .then((response, states) => {
                    // console.log(response.data)
                    var logs_data = response.data

                    res.render('pages/maintenance',
                        {
                            logs_data: logs_data
                         
                        });
                });
        });
});


app.get('/maintenanceinfo/:id', function (req, res) {
    const log_id = req.params.id;

    axios.get('http://127.0.0.1:5000/maintenance/' + log_id
    ).then((response, states) => {
        var logs_data = response.data

        res.render('pages/vehiclesinfo',
            {
                logs_data: logs_data[0]
            });
    });

});

//GARAGE PAGE

app.get('/garage', function (req, res) {
    axios.get('http://127.0.0.1:5000/garage')
        .then((response, states) => {

            var garage_data = response.data

            res.render('pages/garage',
                {
                    garage_data: garage_data[0],
                    states: garage_data[1]
                    

                });
        });
});



app.get('/garageedit/:id', function (req, res) {
    const garage_id = req.params.id;

    axios.get('http://127.0.0.1:5000/garage/' + garage_id
    ).then((response, states) => {
        var garage_data = response.data

        res.render('pages/garageedit',
            {
                garage_data: garage_data[0]
            });
    });

});


app.post('/garage/add', function (req, res) {
    axios.put('http://127.0.0.1:5000/addgarage',
        {
            garage_name: req.body.garage_name,
            phone_number: req.body.phone_number,
            street: req.body.street,
            city: req.body.city,
            state_code_id: req.body.states,
            status: req.body.status,
            garage_hrs: req.body.garage_hrs


        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/garage')
                .then((response, states) => {
                    // console.log(response.data)
                    var garage_data = response.data

                    res.render('pages/garage',
                        {
                            garage_data: garage_data

                        });
                });
        }

        );
});

app.post('/garage/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_garage',
        {
            garage_id: req.body.garage_id,
            garage_name: req.body.garage_name,
            phone_number: req.body.phone_number,
            street: req.body.street,
            city: req.body.city,
            state_code_id: req.body.states,
            status: req.body.status,
            garage_hrs: req.body.garage_hrs


        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/garage')
                .then((response, states) => {
                    // console.log(response.data)
                    var garage_data = response.data

                    res.render('pages/garage',
                        {
                            garage_data: garage_data

                        });
                });
        }

        );
});

// PRODUCTS PAGE
app.get('/products', function (req, res) {
    axios.get('http://127.0.0.1:5000/products')
        .then((response) => {

            var products_data = response.data

            res.render('pages/products',
                {
                    products_data: products_data

                });
        });
});


app.post('/add_product', function (req, res) {
    axios.post('http://127.0.0.1:5000/add_product',
        {
            product_name: req.body.product_name,
            product_status: req.body.product_status

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/products')
                .then((response, states) => {
                    // console.log(response.data)
                    var products_data = response.data

                    res.render('pages/products',
                        {
                            products_data: products_data

                        });
                });
        });
});

app.get('/productsinfo', function (req, res) {

    res.render('pages/productsinfo');
});

app.get('/productsinfo/:id', function (req, res) {
    const product_id = req.params.id;

    axios.get('http://127.0.0.1:5000/products/' + product_id
    ).then((response) => {
        var products_data = response.data

        res.render('pages/rolesinfo',
            {
                products_data: products_data[0]
            });
    });

});


app.post('/products/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_product',
        {
            product_id: req.body.product_id,
            product_name: req.body.product_name,
            product_status: req.body.product_status

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/products')
                .then((response) => {
                    // console.log(response.data)
                    var products_data = response.data

                    res.render('pages/products',
                        {
                            products_data: products_data

                        });
                });
        }

        );
});



app.listen(3000);
console.log('3000 is the magic port');
