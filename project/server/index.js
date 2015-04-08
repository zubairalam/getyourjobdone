var express = require('express'),
    router = express.Router(),
    bodyParser = require('body-parser'),
    cookieParser = require('cookie-parser'),
    http = require('http'),
    methodOverride = require('method-override'),
    session = require('express-session'),
    database = require('./config/database'),
    routes = require('./routes');


var app = express();

app.all("/api/*", function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE");
    res.header("Access-Control-Allow-Headers", "Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With");
    return next();
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(methodOverride());
app.use(cookieParser());

app.set('port', process.env.PORT || 5000);
app.set('host', '0.0.0.0');

app.use('/api/v1', routes.customRoutes);
routes.restifyRoutes(app);


app.disable('x-powered-by');

http.createServer(app).listen(
    app.get('port'),
    app.get('host'),
    function () {
        console.log('API Server running on %s:%s', app.get('host'), app.get('port'));
    }
);