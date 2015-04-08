// This file is for developer testing only. contents may change at any one time.

var fs = require('fs'),
    data = require('../config/database');

var Industry = require('../models/industry');

fs.readFile('./json/industry.json', 'utf8', function (err, data) {
    if (err)
        console.log(err);
    data = JSON.parse(data);
    for (var i = 0; i < data.length; i++) {
        var industry = new Industry();
        industry.name = data[i].name;
        console.log(industry.name);
        industry.save();
    }
    console.log('Data imported successfully');

});
