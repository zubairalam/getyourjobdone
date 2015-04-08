var express = require('express'),
    router = express.Router();

exports.urls = [
    //core patterns
    {pattern: '/', view: router.get('/'), name: 'home'},
    {pattern: '/about', view: router.get('/about'), name: 'about'},
    {pattern: '/advertise', view: router.get('/advertise'), name: 'advertise'},
    {pattern: '/careers', view: router.get('/careers'), name: 'careers'},
    {pattern: '/faq', view: router.get('/faq'), name: 'faq'},
    {pattern: '/pricing', view: router.get('/pricing'), name: 'pricing'},
    {pattern: '/privacy', view: router.get('/privacy'), name: 'privacy'},
    {pattern: '/security', view: router.get('/security'), name: 'security'},
    {pattern: '/support', view: router.get('/support'), name: 'support'},
    {pattern: '/terms', view: router.get('/terms'), name: 'terms'},

    // auth patterns
    {pattern: '/login', view: router.get('/login'), name: 'login'},
    {pattern: '/logout', view: router.get('/logout'), name: 'logout'},
    {pattern: '/signup', view: router.get('/signup'), name: 'signup'},
    {pattern: '/forgot', view: router.get('/forgot'), name: 'forgot'},
    {pattern: '/success', view: router.get('/success'), name: 'success'},

    // dashboard patterns
    {pattern: '/dashboard', view: router.get('/dashboard'), name: 'dashboard'}
];
