var express = require('express');
var router = express.Router();

exports.urls = [
    { pattern: '/', view: router.get('/'), name: 'index' }
]