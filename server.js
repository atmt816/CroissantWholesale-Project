// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');
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

app.get('/employees', function(req, res){
    axios.get('http://127.0.0.1:5000/employees')
    .then((response, states)=>{
        // console.log(response.data)
        var employee_data = response.data

        res.render('pages/employees', 
        { employee_data: employee_data[0],
          states: employee_data[1],
          roles: employee_data[2]   
          });
    });
});


app.get('/empinfo/:id', function (req, res) {
    const emp_id = req.params.id;
    
    axios.get('http://127.0.0.1:5000/empinfo/'+ emp_id
    ).then((response, states)=>{
        var employee_data = response.data
        
        res.render('pages/empinfo', 
        {employee_data: employee_data[0]
        });
    });
  
    
});


app.post('/employees/add', function(req, res) {
    axios.post('http://127.0.0.1:5000/employees/add',
     {
        first_name : req.body.first_name,
        last_name : req.body.last_name,
        start_date: req.body.start_date,
        emp_status : req.body.emp_status,
        role_id: req.body.role_id,
        phone: req.body.phone,
        email: req.body.email,
        street: req.body.street,
        city: req.body.city,
        state_code_id: req.body.states,
        zipcode: req.body.zipcode
     }
    )
    .then((response)=>{
        
        res.render('pages/employees');
        
    });
});
// CUSTOMER PAGE


app.get('/customers', function(req, res){
    axios.get('http://127.0.0.1:5000/customers')
    .then((response, states)=>{
        console.log(response.data)
        var customer_data = response.data

        res.render('pages/customers', 
        { customer_data : customer_data   
          });
    });
});

app.get('/custinfo', function (req, res) {
    res.render('pages/custinfo');
});

app.listen(3000);
console.log('3000 is the magic port');
