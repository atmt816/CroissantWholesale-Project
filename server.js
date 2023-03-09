// load the things we need
var express = require('express');
var app = express();
const bodyParser = require('body-parser');
// required module to make calls to a REST API
const axios = require('axios');
const { response } = require('express');
const req = require('express/lib/request');
var selectedID = "";
//app.use(bodyParser.urlencoded());
// set the view engine to ejs
app.set('view engine', 'ejs');

app.get('/', function (req, res) {

    res.render('pages/index');
});

app.get('/login', function (req, res) {

    res.render('pages/login');
});


app.get('/employees', function (req, res) {
    axios.get('http://127.0.0.1:5000/employees')
        .then((response, states) => {
            console.log(response.data)
            var employee_data = response.data

            res.render('pages/employees',
                {
                    employee_data: employee_data
                    //   states: employee_data[1]  
                });
        });
});

app.get('/empinfo', function (req, res) {
    axios.get('http://127.0.0.1:5000/employee_info')
    res.render('pages/empinfo');
});


app.listen(3000);
console.log('3000 is the magic port');
