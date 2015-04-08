var express = require('express'),
    redis = require('../config/redis');

exports.getSetting = (function (req, res) {
    "use strict";
    redis.hget('settings', req.params.key, function (err, value) {
        if (err) {
            res.json({"message": "error!"});
        }
        res.json({'result': value});
    });
});

exports.getSettings = (function (req, res) {
    "use strict";
    redis.hgetall('settings', function (err, values) {
        if (err) {
            res.json({"message": "error!"});
        }
        res.json(values);
    });
});

exports.setSetting = (function (req, res) {
    "use strict";
    redis.hset(['settings', req.body.key, req.body.value], function (err, value) {
        if (err) {
            res.json({"message": "error!"});
        }
        res.json({"message": "Setting added successfully"});
    });
});

exports.deleteSetting = (function (req, res) {
    "use strict";
    redis.hdel(['settings', req.params.key], function (err, value) {
        if (err) {
            res.json({"message": "error!"});
        }
        res.json({"message": value});
    });
});
