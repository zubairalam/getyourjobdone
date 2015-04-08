var express = require('express'),
    bodyParser = require('body-parser'),
    favicon = require('serve-favicon'),
    http = require('http'),
    morgan = require('morgan'),
    swig = require('swig'),
    path = require('path'),
    stylus = require('stylus'),
    urls = require('urls');

var router = require('./routes');
var patterns = require('./routes/patterns');

var app = express();


app.engine('html', swig.renderFile);

app.set('view engine', 'html');
app.set('view cache', false);
swig.setDefaults({ cache: false });
// app.set('view engine', 'jade');



app.set('views', path.join(__dirname, '/public/views'));


app.use(bodyParser.urlencoded({extended: true}));
app.use(favicon(path.join(__dirname, '/public/img/favicon.ico')));
app.use(express.static(path.join(__dirname, '/public')));
app.use(stylus.middleware(path.join(__dirname, '/public/css')));
app.use(morgan('combined'));

app.locals.pretty = true; // for development mode only.

app.set('host', '0.0.0.0');
app.set('port', process.env.PORT || 3000);

app.use('/', router);

app.disable('x-powered-by');


urls(patterns.urls, app);

http.createServer(app).listen(
    app.get('port'),
    app.get('host'),
    function () {
        console.log('Web Server running on ' + app.get('host') + ':' + app.get('port'));
    }
);