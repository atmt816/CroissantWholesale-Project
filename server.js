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
var moment = require('moment');
app.locals.moment = moment;


// set the view engine to ejs


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



app.get("/home", async (req, res, next) => {

    let chartApi;
    let weekly_data;
    let vendinv_data;
    let prodcount_data;

    try {
        chartApi = await axios.get("http://127.0.0.1:5000/monthlyordercount");
        weekly_data = await axios.get('http://127.0.0.1:5000/weeklyfulfillmentreport');
        vendinv_data = await axios.get('http://127.0.0.1:5000/vendorinventoryreport');
        prodcount_data = await axios.get('http://127.0.0.1:5000/productcounter');
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
                            roles: employee_data[2],
                            success: 'The new employee has been added.'
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
                            success: 'The employee has been updated.',
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
                            roles_data: roles_data,
                            sucess: "The new role has been added."
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
                            roles_data: roles_data,
                            success: 'The role has been updated.'
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
                            states: customer_data[1],
                            success: 'The new customer has been added.'
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
                            states: customer_data[1],
                            success: 'The customer has been updated.'

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
                            roles: vendor_data[2],
                            success: 'The new vendor has been added.'
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
                            states: vendor_data[1],
                            success: 'The vendor has been updated.'

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
                            vehicles_data: vehicles_data,
                            success: 'The vehicle has been added.'
                         
                        });
                });
        });
});

app.get('/vehiclesinfo/:id', function (req, res) {
    const vehicle_id = req.params.id;

    axios.get('http://127.0.0.1:5000/vehicles/' + vehicle_id
    ).then((response) => {
        var vehicles_data = response.data

        res.render('pages/vehiclesinfo',
            {
                vehicles_data: vehicles_data[0],
                maintenance_info: vehicles_data[1]
            });
    });

});

app.post('/vehicles/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_vehicle',
        {
            vehicle_id: req.body.vehicle_id,
            license_plate: req.body.license_plate,
            make: req.body.make,
            model: req.body.model,
            vin: req.body.vin,
            status : req.body.status

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/vehicles')
                .then((response) => {
                    // console.log(response.data)
                    var vehicles_data = response.data

                    res.render('pages/vehicles',
                        {
                            vehicles_data: vehicles_data,
                            success: 'The vehicle has been updated.'

                        });
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
                    logs_data: logs_data[0],
                    garage: logs_data[1],
                    vehicles: logs_data[2],
                

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
    .then((response, states) => {
        axios.get('http://127.0.0.1:5000/maintenance')
        .then((response) => {
        var logs_data = response.data

            res.render('pages/maintenance',
                {
                    logs_data: logs_data[0],
                    garage: logs_data[1],
                    vehicles: logs_data[2],
                    success: 'The maintenance log has been added.'
                });
                });
        
});
});



app.get('/maintenanceinfo/:id', function (req, res) {
    const log_id = req.params.id;

    axios.get('http://127.0.0.1:5000/maintenance/' + log_id
    ).then((response, states) => {
        var logs_data = response.data

        res.render('pages/maintenanceinfo',
            {
                logs_data: logs_data
            });
    });

});

app.post('/maintenance/delete', function (req, res) {
    axios.put('http://127.0.0.1:5000/deletemaintenance',
        {
            log_id:req.body.log_id

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/maintenance')
                .then((response, states) => {
                    // console.log(response.data)
                    var logs_data = response.data

                    res.render('pages/maintenance',
                        {
                            logs_data: logs_data[0],
                            garage: logs_data[1],
                            vehicles: logs_data[2],
                            success: 'The maintenance log has been deleted.'
                        });
                        
                });
        }

        );
});

app.post('/maintenance/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_maintenance_log',
        {
            log_id:req.body.log_id,
            date: req.body.date,
            status: req.body.status,
            note: req.body.note

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/maintenance')
                .then((response, states) => {
                    // console.log(response.data)
                    var logs_data = response.data

                    res.render('pages/maintenance',
                        {
                            logs_data: logs_data[0],
                            garage: logs_data[1],
                            vehicles: logs_data[2],
                            success: 'The maintenance log has been updated.'
                        });
                });
        }

        );
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
                garage_data: garage_data[0],
                states: garage_data[1]
            });
    });

});


app.post('/garage/add', function (req, res) {
    axios.post('http://127.0.0.1:5000/addgarage',
        {
            garage_name: req.body.garage_name,
            phone: req.body.phone,
            street: req.body.street,
            city: req.body.city,
            state_code_id: req.body.states,
            zipcode: req.body.zipcode,
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
                            garage_data: garage_data[0],
                            states: garage_data[1],
                            success: 'The auto shop has been added.'

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
            phone: req.body.phone,
            street: req.body.street,
            city: req.body.city,
            state_code_id: req.body.states,
            zipcode: req.body.zipcode,
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
                            garage_data: garage_data[0],
                            states: garage_data[1],
                            success: 'The auto shop has been updated.'


                        });
                });
        }

        );
});

// INVOICES PAGE
app.get('/invoices', function (req, res) {
    axios.get('http://127.0.0.1:5000/invoices')
        .then((response) => {

            var invoice_data = response.data

            res.render('pages/invoices',
                {
                    invoice_data: invoice_data

                });
        });
});

app.get('/invoicesinfo', function (req, res) {

    res.render('pages/invoicesinfo');
});


app.get('/invoices/:id', function (req, res) {
    const invoice_id = req.params.id;

    axios.get('http://127.0.0.1:5000/invoices/' + invoice_id
    ).then((response) => {
        var invoice_data = response.data

        res.render('pages/invoiceinfo',
            {
                invoice_data: invoice_data[0],
                customer_info: invoice_data[1],
                order_info: invoice_data[2],
                delivery_date: invoice_data[3]
            });
    });

});


app.post('/invoices/update', function (req, res) {
    axios.put('http://127.0.0.1:5000/update_invoices',
        {
            invoice_id: req.body.invoice_id,
            customer_id: req.body.customer_id,
            invoice_date: req.body.invoice_date,
            invoice_total: req.body.invoice_total,
            payment_status: req.body.payment_status,
            date_paid: req.body.date_paid

        }
    )
        .then((response) => {
            axios.get('http://127.0.0.1:5000/invoices')
                .then((response) => {
                    // console.log(response.data)
                    var invoice_data = response.data

                    res.render('pages/invoices',
                        {
                            invoice_data: invoice_data,
                            success: 'The invoice has been updated.'
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
                            products_data: products_data,
                            success: 'The product has been added.'

                        });
                });
        });
});

app.get('/productsinfo', function (req, res) {

    res.render('pages/productsinfo');
});

app.get('/products/:id', function (req, res) {
    const product_id = req.params.id;

    axios.get('http://127.0.0.1:5000/products/' + product_id
    ).then((response) => {
        var products_data = response.data

        res.render('pages/productsinfo',
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
                            products_data: products_data,
                            success: 'The product has been updated.'

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

app.post('/orders/delete', function (req, res) {
    axios.delete('http://127.0.0.1:5000/orders_delete',
        {
            order_id: req.body.order_id
        }
    ).then((response, states) => {
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

app.get('/bestsellers', function (req, res) {
    axios.get('http://127.0.0.1:5000/lifetimebestsellers')
        .then((response) => {

            var best_sell_data = response.data

            res.render('pages/bestsellers',
                {
                    best_sell_data: best_sell_data
                    

                });
        });
});


//ORDERS page

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

app.post('/orders/delete', function (req, res) {
    axios.delete('http://127.0.0.1:5000/orders_delete',
        {
            order_id: req.body.order_id
        }
    ).then((response, states) => {
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


app.listen(3000);
console.log('3000 is the magic port');
