var fs = require('fs'),
    rsvp = require('rsvp');

var readFile = function (filename) {
    var promise = new rsvp.Promise(function (resolve, reject) {
        fs.readFile('recipeitems-latest.json', {encoding: 'utf-8'}, function (err, data) {
            if (err) {
                return reject(err);
            }
            resolve(data);
        });
    });
    return promise;
};

var dataHandler = function (data) {
    if (undefined != data) {
        console.log(data.split('\n'));
    }
};

var errorHandler = function (error) {
    if (undefined != error) {
        console.log(error)
    }
};

readFile()
    .then(dataHandler, errorHandler);

