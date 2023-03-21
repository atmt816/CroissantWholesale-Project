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
                customer_data: customer_data[0]
                
            });
    });

});


// ORDER PAGE

app.get('/orders', function (req, res) {
    axios.get('http://127.0.0.1:5000/orders')
        .then((response) => {
            var order_data = response.data

            res.render('pages/orders',
                {
                    order_data: order_data[0],
                    states: order_data[1],
                    customers: order_data[2],
                    customer_contact: order_data[3],
                    products: order_data[4]
                });
        });
});


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



app.listen(3000);
console.log('3000 is the magic port');
