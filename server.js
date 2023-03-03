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
// set the view engine to ejs
app.set('view engine', 'ejs');

app.get('/', function (req, res) {

    res.render('pages/index');
});

app.listen(5000);
console.log('5000 is the magic port');