var express = require('express'),
    router = express.Router();

exports.urls = [
    //core patterns
    {pattern: '/', view: router.get('/'), name: 'home'}
];